from typing import Optional
import re
import json

class Client:
    def __init__(self, last_name: str, first_name: str, patronymic: str, phone: str):

        self._last_name: str = ""
        self._first_name: str = ""
        self._patronymic: str = ""
        self._phone: str = ""
        #валидация в сеттерах
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.phone = phone

    @staticmethod
    def validate_name(value: str, field_label: str) -> str:
        if not value or str(value).strip() == "":
            raise ValueError(f"{field_label} обязателен")
        s = " ".join(str(value).split())
        if not re.fullmatch(r"[A-Za-zА-Яа-яЁё'\- ]+", s):
            raise ValueError(f"{field_label} содержит недопустимые символы")
        return s.capitalize()

    @staticmethod
    def validate_phone(value: str, field_label: str) -> str:
        if not value or str(value).strip() == "":
            raise ValueError(f"{field_label} обязателен")
        digits = re.sub(r"\D", "", str(value))
        if not (10 <= len(digits) <= 15):
            raise ValueError(f"{field_label} должен содержать от 10 до 15 цифр")
        return "+" + digits

    #Универсальный сеттер
    def _set_field(self, field_name: str, value, validator, *args):
        validated_value = validator(value, *args) if args else validator(value)
        setattr(self, f"_{field_name}", validated_value)

    # Свойства (инкапсуляция)
    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        self._set_field("last_name", value, Client.validate_name, "Фамилия")

    @property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        self._set_field("first_name", value, Client.validate_name, "Имя")

    @property
    def patronymic(self) -> str:
        return self._patronymic

    @patronymic.setter
    def patronymic(self, value: str):
        self._set_field("patronymic", value, Client.validate_name, "Отчество")

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str):
        self._set_field("phone", value, Client.validate_phone, "Телефон")

    # Методы
    def short_str(self) -> str:
        initials = f"{self.first_name[0]}.{self.patronymic[0]}." if self.patronymic else f"{self.first_name[0]}."
        return f"{self.last_name} {initials} Tel:{self.phone}"

    def full_str(self) -> str:
        return f"{self.last_name} {self.first_name} {self.patronymic}, Телефон: {self.phone}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Client):
            return False
        return (
                self.last_name == other.last_name and
                self.first_name == other.first_name and
                self.patronymic == other.patronymic and
                self.phone == other.phone
        )

    # Альтернативные конструкторы
    @classmethod
    def from_csv(cls, csv_str: str):
        parts = [p.strip() for p in csv_str.strip().split(",")]
        if len(parts) != 4:
            raise ValueError("CSV для ClientSummary: last,first,patronymic,phone")
        return cls(parts[0], parts[1], parts[2], parts[3])

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["last_name"], data["first_name"], data["patronymic"], data["phone"])

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls.from_dict(data)

# Полный класс: BigClient
class BigClient(Client):

    #Полная версия клиента: client_id + email.
    def __init__(self, *args, **kwargs):
        self._client_id: Optional[int] = None
        self._email: str = ""
        if len(args) == 1 and isinstance(args[0], str):  # CSV
            parts = [p.strip() for p in args[0].strip().split(",")]
            if len(parts) != 6:
                raise ValueError("CSV для Client: client_id,last,first,patronymic,phone,email")
            client_id, last, first, patr, phone, email = parts
            client_id = int(client_id)
        elif len(args) == 1 and isinstance(args[0], dict):  # dict
            d = args[0]
            client_id = d["client_id"]
            last = d["last_name"]
            first = d["first_name"]
            patr = d["patronymic"]
            phone = d["phone"]
            email = d["email"]
        else:  # kwargs
            client_id = kwargs.get("client_id")
            last = kwargs.get("last_name")
            first = kwargs.get("first_name")
            patr = kwargs.get("patronymic")
            phone = kwargs.get("phone")
            email = kwargs.get("email")

        super().__init__(last, first, patr, phone)

        self.client_id = client_id
        self.email = email

    #Валидаторы
    @staticmethod
    def validate_client_id(value: int) -> int:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("client_id должен быть положительным и целым числом")
        return value

    @staticmethod
    def validate_email(value: str) -> str:
        if not value or str(value).strip() == "":
            raise ValueError("Email обязателен")
        s = str(value).strip()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", s):
            raise ValueError("Некорректный email")
        return s.lower()

    # ---------- Свойства ----------
    @property
    def client_id(self) -> int:
        return self._client_id

    @client_id.setter
    def client_id(self, value: int):
        self._set_field("client_id", value, BigClient.validate_client_id)

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        self._set_field("email", value, BigClient.validate_email)

    # ---------- Методы ----------
    def full_str(self) -> str:
        return (f"Client(id={self.client_id}): {self.last_name} {self.first_name} {self.patronymic}, "
                f"Телефон: {self.phone}, Email: {self.email}")

    def __eq__(self, other) -> bool:
        if not isinstance(other, BigClient):
            return False
        return self.client_id == other.client_id

    # ---------- Альтернативные конструкторы ----------
    @classmethod
    def from_csv(cls, csv_str: str):
        return cls(csv_str)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data)

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls.from_dict(data)

# Демонстрация
if __name__ == "__main__":
    c1 = BigClient(
        client_id=1,
        last_name="Дедушкин",
        first_name="Серафим",
        patronymic="Иванович",
        phone="+7 921 123-45-67",
        email="ivanovich@mail.com"
    )
    print(c1.full_str())
    print(c1.short_str())

    c2 = BigClient("2,Бабушкина,Марфа,Петровна,+7 999 555-55-55,petrovna@mail.com")
    print(c2.full_str())
