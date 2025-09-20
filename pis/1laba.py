import re

class Client:
    FIELDS = ["client_id", "last_name", "first_name", "otch", "address", "phone", "email", "driver_license"]

    def __init__(self, client_id, last_name, first_name, address, phone, driver_license, otch=None, email=None):
        self.client_id = client_id
        self.last_name = last_name
        self.first_name = first_name
        self.address = address
        self.phone = phone
        self.driver_license = driver_license
        self.otch = otch
        self.email = email

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, value):
        value = int(value)
        if value <= 0:
            raise ValueError("client_id должен быть положительным целым числом")
        self._client_id = value

    @staticmethod
    def validate_name(value, field_name):
        value = str(value).strip()
        if not value or not value.replace(" ", "").isalpha():
            raise ValueError(f"{field_name} должно содержать только буквы и не быть пустым")
        return value.title()

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = self.validate_name(value, "Фамилия")

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = self.validate_name(value, "Имя")

    @property
    def otch(self):
        return self._otch

    @otch.setter
    def otch(self, value):
        if value is not None:
            self._otch = self.validate_name(value, "Отчество")
        else:
            self._otch = None

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        value = str(value).strip()
        if not value:
            raise ValueError("Адрес не может быть пустым")
        self._address = value

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        value = str(value)
        if not re.match(r"^\+7\d{10}$", value):
            raise ValueError("Телефон должен быть в формате +7XXXXXXXXXX")
        self._phone = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if value is not None:
            value = str(value)
            if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value):
                raise ValueError("Некорректный email")
        self._email = value

    @property
    def driver_license(self):
        return self._driver_license

    @driver_license.setter
    def driver_license(self, value):
        value = str(value)
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Номер водительского удостоверения должен содержать 10 цифр")
        self._driver_license = value

    def full_repr(self):
        return ", ".join(f"{key}='{getattr(self, key)}'" for key in self.FIELDS if getattr(self, key) is not None)

    def short_repr(self):
        parts = [self.last_name, self.first_name]
        if self.otch:
            parts.append(self.otch)
        return f"{' '.join(parts)} ({self.client_id})"

    def __eq__(self, other):
        if not isinstance(other, Client):
            return False
        return all(getattr(self, f) == getattr(other, f) for f in self.FIELDS)

    def __repr__(self):
        return self.full_repr()


client1 = Client(
    client_id=1,
    last_name="Петров",
    first_name="Александр",
    otch="Сергеевич",
    address="г.Москва, ул.Ленина, д.10",
    phone="+79123488567",
    driver_license="1234567890",
    email="ivanov@mail.ru"
)

client2 = Client(
    client_id=2,
    last_name="Петров",
    first_name="Пётр",
    address="г.Сочи, ул.Пушкина",
    phone="+79123488567",
    driver_license="0987654321"
)
print(client1)
print(client2)
print(client1.full_repr())
print(client2.full_repr())
print(client1.short_repr())
print(client2.short_repr())
print(client1 == client2)  
