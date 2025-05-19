from page_analyzer.models.base_repo import BaseRepository


class UrlRepository(BaseRepository):

    def get_content(self):
        """Извлекает всю информацию по сайтам"""
        with self.get_cursor() as cur:
            cur.execute("SELECT * FROM urls ORDER BY created_at DESC")
            return [dict(row) for row in cur]

    def get_id(self, id):
        """Извлекает всю информацию по конкретному сайту"""
        with self.get_cursor() as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
            return [dict(row) for row in cur]

    def get_specific_id(self, name):
        """Извлекает информацию по имени сайта"""
        with self.get_cursor() as cur:
            cur.execute("SELECT id FROM urls WHERE name = %s", (name,))
            return [dict(row) for row in cur]

    def save(self, url):
        """Сохраняет сайт"""
        if "id" in url and url["id"]:
            self._update(url)
        else:
            self._create(url)

    def _update(self, url):
        """Обновляет сайт"""
        with self.get_cursor() as cur:
            cur.execute(
                "UPDATE  SET name = %s, created_at = %s WHERE id = %s",
                (url["id"], url["name"], url["created_at"]),
            )

    def _create(self, url):
        """Создает сайт"""
        with self.get_cursor() as cur:
            cur.execute(
                """INSERT INTO urls (name, created_at)
                VALUES (%s, %s) RETURNING id""",
                (url["name"], url["created_at"]),
            )
            id = cur.fetchone()[0]
            url["id"] = id
