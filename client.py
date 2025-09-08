from typing import Optional
import re
import json

class Client:
    def __init__(self, *args, **kwargs):
        self._client_id: Optional[int] = None
        self._last_name: str = ""
        self._first_name: str = ""
        self._patronymic: str = ""
        self._phone: str = ""
        self._email: str = ""

        # CSV строка
        if len(args) == 1 and isinstance(args[0], str):
            line = args[0].strip()
            parts = [p.strip() for p in line.split(",")]
            if len(parts) not in (5, 6):
                raise ValueError("CSV строка должна содержать 5 или 6 значений")
            last_name, first_name, patronymic, phone, email = parts[:5]
            client_id = int(parts[5]) if len(parts) == 6 else None

        # Словарь / JSON
        elif len(args) == 1 and isinstance(args[0], dict):
            data = args[0]
            last_name = data["last_name"]
            first_name = data["first_name"]
            patronymic = data["patronymic"]
            phone = data["phone"]
            email = data["email"]
            client_id = data.get("client_id")

        # Параметры через ключевые аргументы
        else:
            last_name = kwargs.get("last_name")
            first_name = kwargs.get("first_name")
            patronymic = kwargs.get("patronymic")
            phone = kwargs.get("phone")
            email = kwargs.get("email")
            client_id = kwargs.get("client_id")

        # Валидация и присвоение через сеттеры
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.phone = phone
        self.email = email
        if client_id is not None:
            self.client_id = client_id

    @staticmethod
    def validate_client_id(value: int) -> int:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("client_id должен быть положительным числом")
        return value

    @staticmethod
    def validate_name(value: str, field_label: str) -> str:
        if not value or value.strip() == "":
            raise ValueError(f"{field_label} обязателен(а)")
        s = " ".join(value.split())
        if not re.fullmatch(r"[A-Za-zА-Яа-яЁё'\- ]+", s):
            raise ValueError(f"{field_label} содержит недопустимые символы")
        return " ".join(part.capitalize() for part in s.split(" "))

    @staticmethod
    def validate_phone(value: str, field_label: str) -> str:
        if not value or value.strip() == "":
            raise ValueError(f"{field_label} обязателен(а)")
        digits = re.sub(r"\D", "", value)
        if not (10 <= len(digits) <= 15):
            raise ValueError(f"{field_label} должен содержать от 10 до 15 цифр")
        return "+" + digits

    @staticmethod
    def validate_email(value: str) -> str:
        if not value or value.strip() == "":
            raise ValueError("Email обязателен")
        s = value.strip()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", s):
            raise ValueError("Некорректный формат email")
        return s.lower()


    # Универсальный метод для сеттеров (убираем повтор кода)
    def _set_field(self, field_name: str, value, validator, *args):
        validated_value = validator(value, *args) if args else validator(value)
        setattr(self, f"_{field_name}", validated_value)

    # Свойства (инкапсуляция)
    @property
    def client_id(self) -> Optional[int]:
        return self._client_id

    @client_id.setter
    def client_id(self, value: int):
        if self._client_id is not None:
            raise AttributeError("client_id уже установлен")
        self._set_field("client_id", value, Client.validate_client_id)

    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        self._set_field("last_name", value, Client.validate_name, "last_name")

    @property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        self._set_field("first_name", value, Client.validate_name, "first_name")

    @property
    def patronymic(self) -> str:
        return self._patronymic

    @patronymic.setter
    def patronymic(self, value: str):
        self._set_field("patronymic", value, Client.validate_name, "patronymic")

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str):
        self._set_field("phone", value, Client.validate_phone, "Телефон")

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        self._set_field("email", value, Client.validate_email)


    # Методы для вывода и сравнения
    def full_str(self) -> str:
        return (f"Client({self.client_id}): {self.last_name} {self.first_name} "
                f"{self.patronymic}, Телефон: {self.phone}, Email: {self.email}")

    def short_str(self) -> str:
        initials = f"{self.first_name[0]}.{self.patronymic[0]}." if self.patronymic else f"{self.first_name[0]}."
        return f"{self.last_name} {initials}, Тел: {self.phone}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Client):
            return False
        return (self.client_id == other.client_id and
                self.last_name == other.last_name and
                self.first_name == other.first_name and
                self.patronymic == other.patronymic and
                self.phone == other.phone and
                self.email == other.email)


# Класс ClientShort (краткая версия)
class ClientShort(Client):
    def __init__(self, client: Client):
        super().__init__(
            last_name=client.last_name,
            first_name=client.first_name,
            patronymic=client.patronymic,
            phone=client.phone,
            email=client.email,
            client_id=client.client_id
        )

    def full_str(self):
        return self.short_str()

# Пример использования

if __name__ == "__main__":
    # Через отдельные аргументы
    c1 = Client(
        last_name="Иванов",
        first_name="Иван",
        patronymic="Иванович",
        phone="+7 999 123-45-67",
        email="ivanov@mail.com",
        client_id=1
    )

    # Через CSV строку
    c2 = Client("Петров,Пётр,Петрович,+7 999 987-65-43,petrov@mail.com,2")

    # Через словарь / JSON
    data = {
        "last_name": "Сидоров",
        "first_name": "Сидор",
        "patronymic": "Сидорович",
        "phone": "+7 999 555-55-55",
        "email": "sidorov@mail.com",
        "client_id": 3
    }
    c3 = Client(data)

    # Вывод
    print(c1.full_str())
    print(c2.short_str())

    # Сравнение
    print(c1 == c2)

    # Краткая версия через наследование
    cs = ClientShort(c3)
    print(cs.full_str())
