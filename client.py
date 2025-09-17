import re
from typing import Optional, Dict, Any
class Client:
    def __init__(self,
                 client_id: int,
                 last_name: str,
                 first_name: str,
                 patronymic: Optional[str],
                 phone: str,
                 email: str ):
        self.__client_id = self.validate_client_id(client_id)
        self.__last_name = self.validate_last_name(last_name)
        self.__first_name = self.validate_first_name(first_name)
        self.__patronymic = self.validate_patronymic(patronymic)
        self.__phone = self.validate_phone(phone)
        self.__email = self.validate_email(email)

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
            return phone

        def validate_client_id(client_id: int) -> int:
            if not isinstance(client_id, int) or client_id <=0:
                raise ValueError("Поле client_id должно быть целым положительным числом!")
            return client_id

        def validate_last_name(last_name: str) -> str:
            if not isinstance(last_name, str) or not last_name.strip():
                raise ValueError("Поле last_name должно быть непустой строкой!")
            return last_name.strip()

        def validate_first_name(first_name: str) -> str:
            if not isinstance(first_name, str) or not first_name.strip():
                raise ValueError("Поле first_name должно быть непустой строкой!")
            return first_name.strip()

        def validate_patronymic(patronymic: Optional[str]) -> Optional[str]:
            if patronymic is None:
                return None
            if not isinstance(patronymic, str):
                raise ValueError("Поле patronymic должно быть строкой!")
            return patronymic.strip() or None

        def validate_phone(phone: str) -> str:
            if not isinstance(phone, str) or not phone.strip():
                raise ValueError("Поле phone должно быть непустой строкой!")
            phone_clean=phone.strip()
            if not re.compile(r"^[\d\+\-\s\(\)]+$").match(phone_clean):
                raise ValueError("Поле phone содержит недопустимые символы!")
            self.__phone=phone_clean

        def validate_email(email: str) -> str:
            if not isinstance(email, str) or not email.strip():
                raise ValueError("Поле email должно быть непустой строкой!")
            email_clean=email.strip()
            if not re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$").match(email_clean):
                raise ValueError("Поле email не соответствует простому формату адреса!")
            self.__email=email_clean

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
            
