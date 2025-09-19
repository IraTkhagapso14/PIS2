import re
import json

class Client:
    FIELDS = ["client_id", "last_name", "first_name", "otch", "address", "phone", "email", "driver_license"]

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], str):
            s = args[0].strip()
            if s.startswith("{") and s.endswith("}"):
                data = json.loads(s)
            else:
                data = self.parse_csv_with_quotes(s)
            kwargs.update(data)

        for field in self.FIELDS:
            setattr(self, field, kwargs.get(field, None))

    def parse_csv_with_quotes(self, s):
        parts = []
        cur = ""
        in_quotes = False
        for char in s:
            if char == '"':
                in_quotes = not in_quotes
            elif char == ',' and not in_quotes:
                parts.append(cur.strip())
                cur = ""
            else:
                cur += char
        parts.append(cur.strip())
        return dict(zip(self.FIELDS, parts))

    def __setattr__(self, name, value):
        if name == "client_id":
            value = self.validate_client_id(value)
        elif name in ("last_name", "first_name") and value is not None:
            value = self.validate_name(value, "Фамилия" if name == "last_name" else "Имя")
        elif name == "otch" and value is not None:
            value = self.validate_name(value, "Отчество")
        elif name == "address" and value is not None:
            value = self.validate_address(value)
        elif name == "phone" and value is not None:
            value = self.validate_phone(value)
        elif name == "email" and value is not None:
            value = self.validate_email(value)
        elif name == "driver_license" and value is not None:
            value = self.validate_driver_license(value)
        super().__setattr__(name, value)

    @staticmethod
    def validate_client_id(value):
        if int(value) <= 0:
            raise ValueError("client_id должен быть положительным целым числом")
        return int(value)

    @staticmethod
    def validate_name(value, field_name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} не может быть пустым")
        if not value.replace(" ", "").isalpha():
            raise ValueError(f"{field_name} должно содержать только буквы")
        return value.strip().title()

    @staticmethod
    def validate_address(value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Адрес не может быть пустым")
        return value.strip()

    @staticmethod
    def validate_phone(value):
        if not re.match(r"^\+7\d{10}$", value):
            raise ValueError("Телефон должен быть в формате +7XXXXXXXXXX")
        return value

    @staticmethod
    def validate_email(value):
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value):
            raise ValueError("Некорректный email")
        return value

    @staticmethod
    def validate_driver_license(value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Номер водительского удостоверения должен содержать 10 цифр")
        return value

    def __repr__(self):
        return ", ".join(f"{key}='{getattr(self, key)}'" for key in self.FIELDS if getattr(self, key) is not None)


client1 = Client(
    client_id=1,
    last_name="Иванов",
    first_name="Александр",
    otch="Сергеевич",
    address="г.Москва, ул.Ленина, д.10",
    phone="+79161234567",
    driver_license="1234567890",
    email="ivanov@mail.ru"
)

client2 = Client('2,Петров,Пётр,Иванович,"г.Сочи, ул.Пушкина",+79261234567,petrov@mail.ru,0987654321')

client3 = Client('{"client_id":3,"last_name":"Сидоров","first_name":"Сидор","otch":"Сидорович","address":"г.Казань, ул.Кремлёвская, д.1","phone":"+79371934567","email":"sidorov@mail.ru","driver_license":"1122334455"}')

print(client1)
print(client2)
print(client3)
