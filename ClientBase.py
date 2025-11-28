from abc import ABC, abstractmethod
from typing import List, Optional
from Client import Client

class ClientBase(ABC):
    def __init__(self):
        self.data: List[Client] = []
        self._load()  # загрузка данных при создании объекта

    # Абстрактные методы для чтения и записи
    @abstractmethod
    def _load(self) -> None:
        pass

    @abstractmethod
    def _save(self) -> None:
        pass

    # Получение объекта по ID
    def get_by_id(self, client_id: int) -> Optional[Client]:
        for client in self.data:
            if client.get_client_id() == client_id:
                return client
        return None

    # Получить k по счету n
    def get_k_n_short_list(self, k: int, n: int) -> List[Client]:
        start = (n - 1) * k
        end = start + k
        return self.data[start:end]

    # Сортировка по фамилии
    def sort_by_last_name(self) -> None:
        self.data.sort(key=lambda c: c.get_last_name())

    # Добавление с проверкой на дубликаты
    def add(self, client: Client) -> Client:
        for c in self.data:
            if (c.get_last_name() == client.get_last_name() and
                c.get_first_name() == client.get_first_name() and
                c.get_patronymic() == client.get_patronymic() and
                c.get_phone() == client.get_phone() and
                c.get_email() == client.get_email()):
                raise ValueError(f"Клиент с такими данными уже существует (ID={c.get_client_id()})!")

        # Генерация нового ID
        new_id = max((c.get_client_id() for c in self.data), default=0) + 1
        client.set_client_id(new_id)
        self.data.append(client)
        self._save()
        return client

    # Заменить объект по ID с проверкой на дубликаты
    def update(self, client_id: int, new_client: Client) -> bool:
        for c in self.data:
            if c.get_client_id() != client_id:
                if (c.get_last_name() == new_client.get_last_name() and
                    c.get_first_name() == new_client.get_first_name() and
                    c.get_patronymic() == new_client.get_patronymic() and
                    c.get_phone() == new_client.get_phone() and
                    c.get_email() == new_client.get_email()):
                    raise ValueError(f"Клиент с такими данными уже существует (ID={c.get_client_id()})!")

        for i, client in enumerate(self.data):
            if client.get_client_id() == client_id:
                new_client.set_client_id(client_id)
                self.data[i] = new_client
                self._save()
                return True
        return False

    # Удалить объект по ID
    def delete(self, client_id: int) -> bool:
        for i, client in enumerate(self.data):
            if client.get_client_id() == client_id:
                del self.data[i]
                self._save()
                return True
        return False

    # Получить количество объектов
    def get_count(self) -> int:
        return len(self.data)
