
from psycopg2.extras import DictCursor

class UrlRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_content(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls ORDER BY created_at DESC")
            return [dict(row) for row in cur]
        
    def get_id(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
            return [dict(row) for row in cur]
        
    def get_specific_id(self, name):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT id FROM urls WHERE name = %s", (name,))
            return [dict(row) for row in cur]   
        
    def save(self, url):
        if "id" in url and url["id"]:
            self._update(url)
        else:
            self._create(url)

    def _update(self, url):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE  SET name = %s, created_at = %s WHERE id = %s",
                (url["id"], url["name"], url["created_at"]),
            )
        self.conn.commit()

    def _create(self, url):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id",
                (url["name"], url["created_at"]),
            )
            id = cur.fetchone()[0]
            url["id"] = id
        self.conn.commit()