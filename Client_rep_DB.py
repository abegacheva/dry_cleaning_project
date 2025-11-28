from Client import Client
from DBConnection import DBConnection

class Client_rep_DB:
    def __init__(self, host, port, user, password, database):
        # Получаем singleton соединение
        self.db = DBConnection(host, port, user, password, database)
        self.conn = self.db.get_connection()

    #получение по айди
    def get_by_id(self, client_id: int):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT client_id, last_name, first_name, patronymic, phone, email "
                "FROM clients WHERE client_id=%s", (client_id,))
            row = cur.fetchone()
            if row:
                return Client(*row)
        return None

    def get_k_n_short_list(self, k: int, n: int):
        offset = (n-1)*k
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT client_id, last_name, first_name, patronymic, phone, email "
                "FROM clients ORDER BY client_id LIMIT %s OFFSET %s", (k, offset))
            rows = cur.fetchall()
            return [Client(*row) for row in rows]

    def add(self, client: Client):
        # Проверка на дубликат
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT client_id FROM clients WHERE last_name=%s AND first_name=%s "
                "AND patronymic=%s AND phone=%s AND email=%s",
                (client.get_last_name(), client.get_first_name(), client.get_patronymic(),
                 client.get_phone(), client.get_email())
            )
            existing = cur.fetchone() #берёт одну строку из результата запроса
            if existing:
                raise ValueError(f"Клиент с такими данными уже существует (ID={existing[0]})!")

            cur.execute(
                "INSERT INTO clients (last_name, first_name, patronymic, phone, email) "
                "VALUES (%s,%s,%s,%s,%s) RETURNING client_id",
                (client.get_last_name(), client.get_first_name(), client.get_patronymic(),
                 client.get_phone(), client.get_email())
            )
            new_id = cur.fetchone()[0]
            self.conn.commit()#Подтверждает изменения в базе данных
            client.set_client_id(new_id)
            return client

    def update(self, client_id: int, new_client: Client):
        with self.conn.cursor() as cur:
            # Проверка на дубликат
            cur.execute(
                "SELECT client_id FROM clients WHERE last_name=%s AND first_name=%s "
                "AND patronymic=%s AND phone=%s AND email=%s AND client_id<>%s",
                (new_client.get_last_name(), new_client.get_first_name(), new_client.get_patronymic(),
                 new_client.get_phone(), new_client.get_email(), client_id)
            )
            existing = cur.fetchone() #берёт одну строку из результата запроса
            if existing:
                raise ValueError(f"Клиент с такими данными уже существует (ID={existing[0]})!")

            cur.execute(
                "UPDATE clients SET last_name=%s, first_name=%s, patronymic=%s, phone=%s, email=%s "
                "WHERE client_id=%s",
                (new_client.get_last_name(), new_client.get_first_name(), new_client.get_patronymic(),
                 new_client.get_phone(), new_client.get_email(), client_id)
            )
            self.conn.commit()
            return cur.rowcount > 0

    def delete(self, client_id: int):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM clients WHERE client_id=%s", (client_id,))
            self.conn.commit()
            return cur.rowcount > 0

    def get_count(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM clients")
            return cur.fetchone()[0]
