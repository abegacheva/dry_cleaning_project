import psycopg2
from psycopg2.extras import DictCursor
from Client import Client

class Client_rep_DB:

    def __init__(self, host, port, user, password, database):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

    # Получить количество элементов
    def get_count(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM clients;")
            return cur.fetchone()[0]

    # Получить объект по ID
    def get_by_id(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM clients WHERE id = %s;", (id,))
            row = cur.fetchone()
            if row is None:
                return None
            return Client(row["id"], row["last_name"], row["first_name"],
                          row["middle_name"], row["phone"], row["email"])

    # Получить k по счету n элементов
    def get_k_n_short_list(self, k, n):
        offset = (n - 1) * k
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                "SELECT * FROM clients ORDER BY id LIMIT %s OFFSET %s;",
                (k, offset)
            )
            rows = cur.fetchall()
            return [Client(r["id"], r["last_name"], r["first_name"],
                           r["middle_name"], r["phone"], r["email"]).__repr__()
                    for r in rows]

    # Добавить объект (генерируем новый ID автоматически)
    def add(self, client: Client):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO clients (last_name, first_name, middle_name, phone, email)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
            """, (client.get_last_name(), client.get_first_name(), client.get_patronymic(),
                  client.get_phone(), client.get_email()))
            new_id = cur.fetchone()[0]
            self.conn.commit()
            client.set_client_id(new_id)
            return new_id

    # Заменить объект по ID
    def update(self, id, client: Client):
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE clients SET
                last_name=%s,
                first_name=%s,
                middle_name=%s,
                phone=%s,
                email=%s
                WHERE id=%s;
            """, (client.get_last_name(), client.get_first_name(), client.get_patronymic(),
                  client.get_phone(), client.get_email(), id))
            self.conn.commit()

    # Удалить объект по ID
    def delete(self, id):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM clients WHERE id = %s;", (id,))
            self.conn.commit()
