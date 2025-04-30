from psycopg2.extras import DictCursor
from page_analyzer.models.pool import db_pool


class UrlCheckRepository:
    def __init__(self, conn):
        conn = db_pool.getconn()
        self.conn = conn
        
    def get_check_id(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC", (id,))
            return [dict(row) for row in cur]
        
    def save(self, check):
        if "id" in check and check["id"]:
            self._update(check)
        else:
            self._create(check)

    def _update(self, check):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE  SET url_id = %s, status_code = %s, h1 = %s, title = %s, description = %s, created_at = %s WHERE id = %s",
                (check["id"], check["url_id"], check["status_code"], check['h1'], check['title'], check['description'], check['created_at']),
            )
        self.conn.commit()

    def _create(self, check):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at) VALUES (%s, %s, %s, %s, %s, %s ) RETURNING id",
                (check["url_id"], check["status_code"], check["h1"], check["title"], check["description"], check["created_at"]),
            )
            id = cur.fetchone()[0]
            check["id"] = id
        self.conn.commit()