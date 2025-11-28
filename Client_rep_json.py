import yaml, os
from Client import Client
from ClientBase import ClientBase

class Client_rep_yaml(ClientBase):
    def __init__(self, filename: str):
        self.filename = filename
        super().__init__()

    def _load(self) -> None:
        if not os.path.exists(self.filename):
            self.data = []
            return

        with open(self.filename, "r", encoding="utf-8") as f:
            try:
                items = yaml.safe_load(f)
            except yaml.YAMLError:
                items = []

        if items is None:
            items = []

        self.data = [Client(**item) for item in items]

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

        with open(self.filename, "w", encoding="utf-8") as f:
            yaml.safe_dump(items, f, allow_unicode=True, sort_keys=False)
