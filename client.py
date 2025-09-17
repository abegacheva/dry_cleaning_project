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

        self.set_client_id(client_id)
        self.set_last_name(last_name)
        self.set_first_name(first_name)
        self.set_patronymic(patronymic)
        self.set_phone(phone)
        self.set_email(email)

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

        def set_client_id(self, client_id: int) ->None:
            if client_id<=0 or not isinstance(client_id, int):
                raise ValueError("Поле client_id должно быть целым положительным числом!")
            self.__client_id=client_id

        def set_last_name(self, last_name: str) ->None:
            if not last_name.strip() or not isinstance(last_name, str):
                raise ValueError("Поле last_name должно быть непустой строкой!")
            self.__last_name=last_name.strip()

        def set_first_name(self, first_name: str) -> None:
            if not first_name.strip() or not isinstance(first_name, str):
                raise ValueError("Поле first_name должно быть непустой строкой!")
            self.__first_name=first_name.strip()

        def set_patronymic(self, patronymic: str) -> None:
            if patronymic is None:
                self.__patronymic=None
                return
            if not isinstance(patronymic, str):
                raise  ValueError("Поле patronymic должно быть строкой!")
            self.__patronymic=patronymic.strip() or None

        def set_phone(self, phone: str) ->None:
            if not isinstance(phone, str) or not phone.strip():
                raise ValueError("Поле phone должно быть непустой строкой!")
            phone_clean=phone.strip()
            if not re.compile(r"^[\d\+\-\s\(\)]+$").match(phone_clean):
                raise ValueError("Поле phone содержит недопустимые символы!")
            self.__phone=phone_clean

        def set_email(self, email: str) -> None:
            if not isinstance(email, str) or not email.strip():
                raise ValueError("Поле email должно быть непустой строкой!")
            email_clean=email.strip()
            if not re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$").match(email_clean):
                raise ValueError("Поле email не соответствует простому формату адреса!")
            self.__email=email_clean
