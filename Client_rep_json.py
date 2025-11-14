import json
import os
from typing import List, Optional
from Client import Client

class Client_rep_json:
    def __init__(self, filename: str):
        self.filename = filename
        self.data: List[Client]=[]
        self._load()

    #Чтение всех значений из файла
    def _load(self) -> None:
        if not os.path.exists(self.filename):
            self.data=[]
            return
        with open(self.filename,"r", encoding="utf-8") as file:
            try:
                items= json.load(file)
            except json.JSONDecodeError:
                items = []
        self.data=[Client(item) for item in items]

    #Запись всех значений в файл
    def _save(self) -> None:
        items=[]
        for client in self.data:
            items.append({
                "client_id": client.get_client_id(),
                "last_name": client.get_last_name(),
                "first_name": client.get_first_name(),
                "patronymic": client.get_patronymic(),
                "phone": client.get_phone(),
                "email": client.get_email()
            })
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(items,file, ensure_ascii = False, indent = 4)

    #Получение объекта по айди
    def get_by_id(self, client_id: int) -> Optional[Client]:
        for client in self.data:
            if client.get_client_id() == client_id:
                return client
        return None

    #Получить список k по счёту n (например вторые 20 -> k=20, n=2)
    def get_k_n_short_list(self, k: int, n: int) -> List[Client]:
        start = (n-1)*k
        end = start + k
        return self.data[start:end]

    #Сортировать эл-ты по выбранному полю
    def sort_by_last_name(self) -> None:
        self.data.sort(key = lambda c: c.get_last_name())

    #Добавить объект (Создать новый айди)
    def add(self, client:Client) -> Client:
        #Нельзя создать копию с другим айди
        for c in self.data:
            if (c.get_last_name() == client.get_last_name() and
                    c.get_first_name() == client.get_first_name() and
                    c.get_patronymic() == client.get_patronymic() and
                    c.get_phone() == client.get_phone() and
                    c.get_email() == client.get_email()):
                raise ValueError("Клиент с такими данными уже существует!")

        #Генерация нового айди
        if self.data:
            new_id = max(c.get_client_id() for c in self.data) + 1
        else:
            new_id = 1

        client.set_client_id(new_id)
        self.data.append(client)
        self._save()
        return client

    #Заменить по айди
    def update(self, client_id: int, new_client: Client) -> bool:
        for i, client in enumerate(self.data):
            if client.get_client_id() == client_id:
                new_client.set_client_id(client_id)
                self.data[i] = new_client
                self._save()
                return True
        return False

    #Удалить по айди
    def delete(self, client_id: int) -> bool:
        for i, client in enumerate(self.data):
            if client.get_client_id() == client_id:
                del self.data[i]
                self._save()
                return True
        return False

    #Получить количество элементов
    def get_count(self) -> int:
        return len(self.data)
