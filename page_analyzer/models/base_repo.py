from contextlib import contextmanager

from psycopg2.extras import DictCursor

from page_analyzer.models.pool import db_pool


class BaseRepository:
    @contextmanager
    def get_cursor(self):
        """Создает курсор"""
        conn = db_pool.getconn()
        try:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                yield cur
                conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            db_pool.putconn(conn)
