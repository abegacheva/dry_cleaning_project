import yaml
import os
from Client import Client
from ClientBase import ClientBase

class Client_rep_yaml(ClientBase):
    """
    Реализует методы _load() и _save() для YAML
    """
    #Чтение всех значений из YAML
    def _load(self) -> None:
        if not os.path.exists(self.filename):
            self.data = []
            return
        with open(self.filename, "r", encoding="utf-8") as file:
            try:
                items = yaml.safe_load(file)
            except yaml.YAMLError:
                items = []
        if items is None:
            items = []
        self.data = [Client(item) for item in items]

    #Запись всех значений в YAML
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
            yaml.safe_dump(items, file, allow_unicode=True, sort_keys=False)
