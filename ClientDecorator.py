from Client import Client
from typing import Callable, List

class ClientDecorator:
    def __init__(self, repo):
        """
        repo - любой объект, который реализует методы:
        get_k_n_short_list(k, n) и get_count()
        """
        self.repo = repo

    def get_k_n_short_list(self, k: int, n: int,
                           filter_func: Callable[[Client], bool] = None,
                           sort_key: Callable[[Client], any] = None) -> List[Client]:
        """
        Получить список объектов с возможностью фильтрации и сортировки
        filter_func: функция фильтрации, принимающая Client -> bool
        sort_key: функция сортировки, принимающая Client -> любое сравнимое значение
        """
        clients = self.repo.get_k_n_short_list(k, n)
        if filter_func:
            clients = list(filter(filter_func, clients))
        if sort_key:
            clients.sort(key=sort_key)
        return clients

    def get_count(self, filter_func: Callable[[Client], bool] = None) -> int:
        """
        Получить количество объектов с возможностью фильтрации
        """
        # Берём все элементы для подсчёта с фильтром
        clients = self.repo.get_k_n_short_list(1000000, 1)
        if filter_func:
            clients = list(filter(filter_func, clients))
        return len(clients)

    def __getattr__(self, attr):
        """
        Делегируем все остальные вызовы методов оригинальному репозиторию
        """
        return getattr(self.repo, attr)
