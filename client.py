import json
import re
from typing import Optional, Dict, Any


class Client:
    def __init__(self, *args, **kwargs ):

        data = self._parse_args(*args,**kwargs)

        self._set_field("client_id", data.get("client_id"))
        self._set_field("last_name", data.get("last_name"))
        self._set_field("first_name", data.get("first_name"))
        self._set_field("patronymic", data.get("patronymic"))
        self._set_field("phone", data.get("phone"))
        self._set_field("email", data.get("email"))

    @staticmethod
    def _parse_args(*args, **kwargs):
        if len(args) == 1:
            first = args[0]
            if isinstance(first, dict):
                return first
            elif isinstance(first, str):
                try:
                    return json.loads(first)
                except json.JSONDecodeError:
                    parts = [p.strip() for p in first.split(",")]
                    if len(parts) == 6:
                        keys = ["client_id", "last_name", "first_name", "patronymic", "phone", "email"]
                        data = dict(zip(keys, parts))
                        data["client_id"] = int(data["client_id"])
                        return data
                    else:
                        raise ValueError("Строка не является корректным JSON или CSV")
            else:
                raise ValueError("Неподдерживаемый тип аргумента")
        elif len(args) == 6:
            keys = ["client_id", "last_name", "first_name", "patronymic", "phone", "email"]
            return dict(zip(keys, args))
        elif kwargs:
            return kwargs
        else:
            raise ValueError("Неверные аргументы конструктора")

    def get_client_id(self) ->int:
        return self.__client_id
    def get_last_name(self) -> str:
        return self.__last_name
    def get_first_name(self) -> str:
        return self.__first_name
    def get_patronymic(self) -> Optional[str]:
        return self.__patronymic
    def get_phone(self)-> str:
        return self.__phone
    def get_email(self) -> str:
        return self.__email


    def __repr__(self) ->str:
        patronymic = f"'{self.__patronymic}'" if self.__patronymic else "None"
        return (f"Client(client_id={self.__client_id}, "
                f"last_name='{self.__last_name}', "
                f"first_name='{self.__first_name}', "
                f"patronymic={patronymic}, "
                f"phone='{self.__phone}', "
                f"email='{self.__email}')")

    def __str__(self) -> str:
        full_name = f"{self.__last_name} {self.__first_name}"
        if self.__patronymic:
            full_name += f" {self.__patronymic}"
        return f"{full_name} ({self.__email}, {self.__phone})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Client):
            return NotImplemented
        return (self.__client_id == other.__client_id
                and self.__last_name == other.__last_name
                and self.__first_name == other.__first_name
                and self.__patronymic == other.__patronymic
                and self.__phone == other.__phone
                and self.__email == other.__email)


    def _set_field(self, field_name: str, value):
        if field_name == "client_id":
            self.__client_id = self.validate_client_id(value)
        elif field_name == "last_name":
            self.__last_name = self.validate_name(value, 'last_name')
        elif field_name == "first_name":
            self.__first_name = self.validate_name(value, 'first_name')
        elif field_name == "patronymic":
            self.__patronymic = self.validate_patronymic(value)
        elif field_name == "phone":
            self.__phone = self.validate_phone(value)
        elif field_name == "email":
            self.__email = self.validate_email(value)
        else:
            raise ValueError(f"Неизвестное поле: {field_name}")

    @staticmethod
    def validate_client_id(client_id: int) -> int:
        if not isinstance(client_id, int) or client_id <=0:
            raise ValueError("Поле client_id должно быть целым положительным числом!")
        return client_id

    @staticmethod
    def validate_name(name: str, type_name: str) -> str:
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"Поле {type_name} должно быть непустой строкой!")
        pattern = r"^[A-Za-zА-ЯЁа-яё]+(?:[-\s][A-Za-zА-ЯЁа-яё]+)*$"
        if not re.fullmatch(pattern, name.strip()):
            raise ValueError(f"В {type_name} содержатся недопустимые символы")
        parts = name.strip().split()
        normalized = []
        for part in parts:
            subparts = part.split('-')
            normalized.append('-'.join(s.capitalize() for s in subparts))
        return " ".join(normalized)
        return name.strip().capitalize()

    @staticmethod
    def validate_patronymic(patronymic: Optional[str]) -> Optional[str]:
        if patronymic is None or patronymic == '':
            return None

        return Client.validate_name(patronymic, 'patronymic')

    @staticmethod
    def validate_phone(phone: str) -> str:
        if not isinstance(phone, str) or not phone.strip():
            raise ValueError("Поле phone должно быть непустой строкой!")
        phone_clean=phone.strip()
        if not re.match(r"^\+\d+\s\d{3}\s\d{3}-\d{2}-\d{2}$", phone_clean):
            raise ValueError("Поле phone содержит недопустимые символы!")
        return phone_clean

    @staticmethod
    def validate_email(email: str) -> str:
        if not isinstance(email, str) or not email.strip():
            raise ValueError("Поле email должно быть непустой строкой!")
        email_clean=email.strip()
        if not re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$").match(email_clean):
            raise ValueError("Поле email не соответствует простому формату адреса!")
        return email_clean


    def set_client_id(self, client_id: int) -> None:
        self.__client_id = self.validate_client_id(client_id)

    def set_last_name(self, last_name: str) -> None:
        self.__last_name = self.validate_name(last_name, 'last_name')

    def set_first_name(self, first_name: str) -> None:
        self.__first_name = self.validate_name(first_name, 'first_name')

    def set_patronymic(self, patronymic: Optional[str]) -> None:
        self.__patronymic = self.validate_patronymic(patronymic)

    def set_phone(self, phone: str) -> None:
        self.__phone = self.validate_phone(phone)

    def set_email(self, email: str) -> None:
        self.__email = self.validate_email(email)


class RegularClient(Client):
    def __init__(self, client: Client, address: Optional[str] = None, discount: float = 0.0):
        super().__init__(
            client_id=client.get_client_id(),
            last_name=client.get_last_name(),
            first_name=client.get_first_name(),
            patronymic=client.get_patronymic(),
            phone=client.get_phone(),
            email=client.get_email()
        )
        # Добавленные поля
        self.address = address
        self.discount = self.validate_discount(discount)

        # Полное имя (без инициалов)
        parts = [self.get_last_name(), self.get_first_name()]
        if self.get_patronymic():
            parts.append(self.get_patronymic())
        self.full_name = " ".join(parts)

    @staticmethod
    def validate_discount(discount: float) -> float:
        if not isinstance(discount, (int, float)) or not (0 <= discount <= 100):
            raise ValueError("Скидка должна быть числом от 0 до 100!")
        return float(discount)

    def get_client_id(self):
        return super().get_client_id()

    def get_address(self):
        return self.address

    def get_discount(self):
        return self.discount

    def __repr__(self):
        return (f"RegularClient(client_id={super().get_client_id()}, "
                f"full_name='{self.full_name}', "
                f"address='{self.address}', "
                f"discount={self.discount}%)")

    def __str__(self):
        return (f"{self.full_name} — скидка {self.discount}% "
                f"({self.get_email()}, {self.get_phone()}, адрес: {self.address})")

    def __eq__(self, other):
        if isinstance(other, RegularClient):
            return super().get_client_id() == other.get_client_id()
        return False


if __name__ == '__main__':
    print("\nСоздание через словарь")
    print("--------------------------------------------")
    client_dict = Client({
        "client_id": 1,
        "last_name": "Бабушкина",
        "first_name": "Марфа",
        "patronymic": "Петровна",
        "phone": "+7 912 345-67-89",
        "email": "petrovna1940@gmail.com"
    })
    print(client_dict)
    print(RegularClient(client_dict, address="г. Пермь, ул. Мира, 10", discount=5))
    print("--------------------------------------------")

    print("\nСоздание через JSON-строку")
    print("--------------------------------------------")
    json_str = '{"client_id": 2, "last_name": "Дедушкин", "first_name": "Аркадий", "patronymic": "Петрович", "phone": "+7 999 111-22-33", "email": "petrovich1939@gmail.com"}'
    client_json = Client(json_str)
    print(client_json)
    print(RegularClient(client_json, address="г. Казань, ул. Баумана, 15", discount=10))
    print("--------------------------------------------")

    print("\nСоздание через CSV-строку")
    print("--------------------------------------------")
    csv_str = "3, Холланд, Том, , +7 888 777-66-55, TomHolland@mail.ru"
    client_csv = Client(csv_str)
    print(client_csv)
    print(RegularClient(client_csv, address="Лондон, Бейкер-стрит, 221Б", discount=7.5))
    print("--------------------------------------------")

    print("\nСоздание через позиционные аргументы")
    print("--------------------------------------------")
    client_args = Client(4, "Гослинг", "Райан", None, "+7 123 456-78-90", "superstar@example.com")
    print(client_args)
    print(RegularClient(client_args, address="Лос-Анджелес, Голливуд бульвар, 42", discount=12))
    print("--------------------------------------------")

    print("\nСоздание через именованные аргументы")
    print("--------------------------------------------")
    client_kwargs = Client(
        client_id=5,
        last_name="Кодиков",
        first_name="Программист",
        patronymic="Скриптович",
        phone="+7 321 654-98-76",
        email="superproger@gmail.com"
    )
    print(client_kwargs)
    print(RegularClient(client_kwargs, address="г. Москва, ул. Питона, 3", discount=15))
    print("--------------------------------------------")
