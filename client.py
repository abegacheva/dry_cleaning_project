import json
import re
from typing import Optional, Dict, Any
class Client:
    def __init__(self, *args, **kwargs ):

        data = {}

        if len(args) == 1:
            first = args[0]
            if isinstance(first, dict):
                data = first
            elif isinstance(first, str):
                try:
                    data = json.loads(first)
                except json.JSONDecodeError:
                    parts = [p.strip() for p in first.split(",")]
                    if len(parts) == 6:
                        keys = ["client_id", "last_name", "first_name", "patronymic", "phone", "email"]
                        data = dict(zip(keys, parts))
                        try:
                            data["client_id"] = int(data["client_id"])
                        except ValueError:
                            raise ValueError("client_id в CSV должен быть целым числом")
                    else:
                        raise ValueError("Строка не является корректным JSON или CSV")
            else:
                raise ValueError("Неподдерживаемый тип аргумента")

        elif len(args) == 6:
            keys = ["client_id", "last_name", "first_name", "patronymic", "phone", "email"]
            data = dict(zip(keys, args))

        elif kwargs:
            data = kwargs

        else:
            raise ValueError("Неверные аргументы конструктора")

        self._set_field("client_id", data.get("client_id"))
        self._set_field("last_name", data.get("last_name"))
        self._set_field("first_name", data.get("first_name"))
        self._set_field("patronymic", data.get("patronymic"))
        self._set_field("phone", data.get("phone"))
        self._set_field("email", data.get("email"))


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
        return (f"Client(client_id={self.__client_id}, "
                f"last_name='{self.__last_name}', "
                f"first_name='{self.__first_name}', "
                f"patronymic='{self.__patronymic}', "
                f"phone='{self.__phone}', "
                f"email='{self.__email}')")

    def __str__(self) -> str:
        return f"{self.__last_name} {self.__first_name} {self.__patronymic} ({self.__email})"

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
            self.__last_name = self.validate_last_name(value)
        elif field_name == "first_name":
            self.__first_name = self.validate_first_name(value)
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
    def validate_last_name(last_name: str) -> str:
        if not isinstance(last_name, str) or not last_name.strip():
            raise ValueError("Поле last_name должно быть непустой строкой!")
        return last_name.strip()

    @staticmethod
    def validate_first_name(first_name: str) -> str:
        if not isinstance(first_name, str) or not first_name.strip():
              raise ValueError("Поле first_name должно быть непустой строкой!")
        return first_name.strip()

    @staticmethod
    def validate_patronymic(patronymic: Optional[str]) -> Optional[str]:
        if patronymic is None:
            return None
        if not isinstance(patronymic, str):
            raise ValueError("Поле patronymic должно быть строкой!")
        return patronymic.strip() or None

    @staticmethod
    def validate_phone(phone: str) -> str:
        if not isinstance(phone, str) or not phone.strip():
            raise ValueError("Поле phone должно быть непустой строкой!")
        phone_clean=phone.strip()
        if not re.compile(r"^[\d\+\-\s\(\)]+$").match(phone_clean):
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
        self.__last_name = self.validate_last_name(last_name)

    def set_first_name(self, first_name: str) -> None:
        self.__first_name = self.validate_first_name(first_name)

    def set_patronymic(self, patronymic: Optional[str]) -> None:
        self.__patronymic = self.validate_patronymic(patronymic)

    def set_phone(self, phone: str) -> None:
        self.__phone = self.validate_phone(phone)

    def set_email(self, email: str) -> None:
        self.__email = self.validate_email(email)

