import json
import os
from Client import Client
from ClientBase import ClientBase

class Client_rep_json(ClientBase):
    """
    Реализует методы _load() и _save() для JSON
    """
    #Чтение всех значений из JSON
    def _load(self) -> None:
        if not os.path.exists(self.filename):
            self.data = []
            return
        with open(self.filename, "r", encoding="utf-8") as file:
            try:
                items = json.load(file)
            except json.JSONDecodeError:
                items = []
        self.data = [Client(item) for item in items]

    #Запись всех значений в JSON ---
    def _save(self) -> None:
        items = []
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
            json.dump(items, file, ensure_ascii=False, indent=4)
