from ClientBase import ClientBase
from Client_rep_DB import Client_rep_DB
from Client import Client

class ClientDBAdapter(ClientBase):
    def __init__(self, host, port, user, password, database):
        # Не используем self.data напрямую
        self.db_repo = Client_rep_DB(host, port, user, password, database)
        self.data = []  # для совместимости с ClientBase
        super().__init__()

    def _load(self) -> None:
        # Загружаем все объекты из БД в self.data для совместимости
        self.data = self.db_repo.get_k_n_short_list(1000000, 1)  # берём все записи

    def _save(self) -> None:
        # В БД изменения сохраняются сразу, поэтому можно просто пропустить
        pass

    # Переопределяем методы, чтобы делегировать в DB репозиторий
    def add(self, client: Client) -> Client:
        result = self.db_repo.add(client)
        self._load()
        return result

    def update(self, client_id: int, new_client: Client) -> bool:
        result = self.db_repo.update(client_id, new_client)
        self._load()
        return result

    def delete(self, client_id: int) -> bool:
        result = self.db_repo.delete(client_id)
        self._load()
        return result

    def get_by_id(self, client_id: int):
        return self.db_repo.get_by_id(client_id)

    def get_k_n_short_list(self, k: int, n: int):
        return self.db_repo.get_k_n_short_list(k, n)

    def get_count(self):
        return self.db_repo.get_count()
