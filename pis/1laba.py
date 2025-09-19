import re

class Client():
    FIELDS = ["client_id", "last_name", "first_name", "otch", "address", "phone", "email", "driver_license"]
    
    def __init__(self, client_id, last_name, first_name, address, phone, driver_license, otch=None, email=None):
        self.client_id = client_id
        self.last_name = last_name
        self.first_name = first_name
        self.otch = otch
        self.address = address
        self.phone = phone
        self.driver_license = driver_license
        self.email = email

    def __setattr__(self, name, value):
        if name == "client_id":
            value = self.validate_client_id(value)
        elif name in ("last_name", "first_name"):
            value = self.validate_name(value, "Фамилия" if name == "last_name" else "Имя")
        elif name == "otch" and value is not None:
            value = self.validate_name(value, "Отчество")
        elif name == "address":
            value = self.validate_address(value)
        elif name == "phone":
            value = self.validate_phone(value)
        elif name == "email" and value is not None:
            value = self.validate_email(value)
        elif name == "driver_license":
            value = self.validate_driver_license(value)
            
        super().__setattr__(name, value)

    @staticmethod
    def validate_client_id(value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("client_id должен быть положительным целым числом")
        return value

    @staticmethod
    def validate_name(value, field_name):
        if not value or not value.strip():
            raise ValueError(field_name+" " +"не может быть пустым")
        if not value.replace(" ", "").isalpha():
            raise ValueError(field_name+" " +"должно содержать только буквы")
        return value.strip().title()

    @staticmethod
    def validate_address(value):
        if not value or not value.strip():
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
       return ", ".join(f"{key}='{getattr(self, key)}'" for key in self.FIELDS if hasattr(self, key))

try:
    client = Client(
        client_id=1,
        last_name="Иванов",
        first_name="Александр",
        otch="Сергеевич",
        address="г.Москва, ул.Ленина, д.10",
        phone="+79161234567",
        driver_license="1234567890",
        email="ivanov@mail.ru"
    )
    print(client)

except ValueError as e:
    print("Ошибка создания клиента:", e)
