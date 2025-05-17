from page_analyzer.models.base_repo import BaseRepository


class UrlCheckRepository(BaseRepository):

    def get_check_id(self, id):
        with self.get_cursor() as cur:
            cur.execute(
                "SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC ",
                (id,)
                )
            return [dict(row) for row in cur]

    def save(self, check):
        if "id" in check and check["id"]:
            self._update(check)
        else:
            self._create(check)

    def _update(self, check):
        with self.get_cursor() as cur:
            cur.execute(
                """
                UPDATE url_checks
                SET url_id = %s,
                status_code = %s,
                h1 = %s,
                title = %s,
                description = %s,
                created_at = %s
                WHERE id = %s
                """,
                (
                    check["url_id"],
                    check["status_code"],
                    check['h1'],
                    check['title'],
                    check['description'],
                    check['created_at'],
                    check['id']
                ),
            )

    def _create(self, check):
        with self.get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO url_checks (
                url_id,
                status_code,
                h1,
                title,
                description,
                created_at
                ) VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    check["url_id"],
                    check["status_code"],
                    check["h1"],
                    check["title"],
                    check["description"],
                    check["created_at"],
                ),
            )
            id = cur.fetchone()[0]
            check["id"] = id
