import re

class Client:
    def __init__(self, client_id, last_name, first_name, address, phone, driver_license, 
                 otch=None, email=None):
        self._client_id = self.validate_client_id(client_id)
        self._last_name = self.validate_name(last_name, "Фамилия")
        self._first_name = self.validate_name(first_name, "Имя")
        self._otch = otch  
        self._address = self.validate_address(address)
        self._phone = self.validate_phone(phone)
        self._email = self.validate_email(email) if email else None
        self._driver_license = self.validate_driver_license(driver_license)

    @staticmethod
    def validate_client_id(value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("client_id должен быть положительным целым числом")
        return value

    @staticmethod
    def validate_name(value, field_name):
        if not value or not value.strip():
            raise ValueError(field_name+" "+"не может быть пустым")
        if not value.isalpha():
            raise ValueError(field_name +" "+"должно содержать только буквы")
        return value.strip().title()

    @staticmethod
    def validate_address(value):
        if not value or not value.strip():
            raise ValueError("Адрес не может быть пустым")
        return value.strip()

    @staticmethod
    def validate_phone(value):
        pattern = r"^\+7\d{10}$" 
        if not re.match(pattern, value):
            raise ValueError("Телефон должен быть в формате +7XXXXXXXXXX (11 цифр)")
        return value

    @staticmethod
    def validate_email(value):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, value):
            raise ValueError("Некорректный email")
        return value

    @staticmethod
    def validate_driver_license(value):
        if not value or not value.isdigit():
            raise ValueError("Номер водительского удостоверения должен содержать только цифры")
        if len(value)!=10:  
            raise ValueError("Номер водительского удостоверения должен быть длиной 10 цифр")
        return value

    @property
    def client_id(self):
        return self._client_id
    
    @client_id.setter
    def client_id(self, value):
        self._client_id = self.validate_client_id(value)

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
        self._otch = value

    @property
    def address(self):
        return self._address
    
    @address.setter
    def address(self, value):
        self._address = self.validate_address(value)

    @property
    def phone(self):
        return self._phone
    
    @phone.setter
    def phone(self, value):
        self._phone = self.validate_phone(value)

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        self._email = self.validate_email(value)

    @property
    def driver_license(self):
        return self._driver_license
    
    @driver_license.setter
    def driver_license(self, value):
        self._driver_license = self.validate_driver_license(value)

    def __repr__(self):
        return "client_id=" + str(self.client_id) + ", " + \
               "last_name='" + str(self.last_name) + "', " + \
               "first_name='" + str(self.first_name) + "', " + \
               "otch='" + str(self.otch) + "', " + \
               "address='" + str(self.address) + "', " + \
               "phone='" + str(self.phone) + "', " + \
               "email='" + str(self.email) + "', " + \
               "driver_license='" + str(self.driver_license) + "'" 
        
try:
    client = Client(
        client_id=1,
        last_name="Петров",
        first_name="Александр",
        otch="Сергеевич",
        address="г.Краснодар, ул.Красная, д.9",
        phone="+78005553535",
        driver_license="1111111111",
        email="petrovas@yandex.ru"
    )
    print(client)
except ValueError as e:
    print("Ошибка:", e)
