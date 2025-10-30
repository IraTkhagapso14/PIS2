import re

class ClientShort:
    def __init__(self, client_id: int, last_name: str, first_name: str, otch: str = None, contact: str = None):
        self._client_id = self._validate_id(client_id)
        self._last_name = self._validate_name(last_name, "Фамилия")
        self._first_name = self._validate_name(first_name, "Имя")
        self._otch = self._validate_name(otch, "Отчество") if otch else None
        self._contact = contact

    @property
    def client_id(self):
        return self._client_id

    @property
    def last_name(self):
        return self._last_name

    @property
    def first_name(self):
        return self._first_name

    @property
    def otch(self):
        return self._otch

    @property
    def contact(self):
        return self._contact

    @staticmethod
    def _validate_id(value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("client_id должен быть положительным целым числом")
        return value

    @staticmethod
    def _validate_name(value, field_name):
        value = str(value).strip()
        if not value or not value.replace(" ", "").isalpha():
            raise ValueError(f"{field_name} должно содержать только буквы и не быть пустым")
        return value.title()

    def fio_full(self):
        parts = [self.last_name, self.first_name]
        if self.otch:
            parts.append(self.otch)
        return " ".join(parts)

    def fio_short(self):
        initials = f"{self.first_name[0]}."
        if self.otch:
            initials += f"{self.otch[0]}."
        return f"{self.last_name} {initials}"

    def __repr__(self):
        return f"ClientShort(id={self.client_id}, fio='{self.fio_short()}', contact='{self.contact}')"

    def __eq__(self, other):
        if not isinstance(other, ClientShort):
            return False
        return (self.client_id == other.client_id and
                self.fio_short() == other.fio_short() and
                self.contact == other.contact)


class Client(ClientShort):
    FIELDS = ["client_id", "last_name", "first_name", "otch", "address", "phone", "email", "driver_license"]

    def __init__(self, client_id, last_name, first_name, address, phone, driver_license, otch=None, email=None):
        contact = email if email else phone
        super().__init__(client_id, last_name, first_name, otch, contact)
        
        self.address = self._validate_address(address)
        self.phone = self._validate_phone(phone)
        self.email = self._validate_email(email) if email else None
        self.driver_license = self._validate_license(driver_license)

    @staticmethod
    def _validate_address(value):
        value = str(value).strip()
        if not value:
            raise ValueError("Адрес не может быть пустым")
        return value

    @staticmethod
    def _validate_phone(value):
        value = str(value)
        if not re.match(r"^\+7\d{10}$", value):
            raise ValueError("Телефон должен быть в формате +7XXXXXXXXXX")
        return value

    @staticmethod
    def _validate_email(value):
        value = str(value)
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value):
            raise ValueError("Некорректный email")
        return value

    @staticmethod
    def _validate_license(value):
        value = str(value)
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Номер водительского удостоверения должен содержать 10 цифр")
        return value

    def full_repr(self):
        return ", ".join(f"{key}='{getattr(self, key)}'" for key in self.FIELDS if getattr(self, key) is not None)

    def short_repr(self):
        return f"{self.fio_full()} ({self.client_id})"

    def __repr__(self):
        return self.full_repr()

    def __eq__(self, other):
        if not isinstance(other, Client):
            return False
        return all(getattr(self, f) == getattr(other, f) for f in self.FIELDS)

    def to_short(self):
        return ClientShort(self.client_id, self.last_name, self.first_name, self.otch, self.contact)


if __name__ == "__main__":
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

    print("Полные клиенты")
    print(client1.full_repr())
    print(client2.full_repr())

    print("Краткие версии")
    print(client1.to_short())
    print(client2.to_short())
