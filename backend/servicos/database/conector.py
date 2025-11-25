from typing import Any
import psycopg2
from psycopg2.extras import DictCursor

class DatabaseManager:
    "Classe de Gerenciamento do database"

    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            dbname="biblioteca",
            user="postgres",
            password="root",
            host="127.0.0.1",
            port=5432,
        )
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)

    def execute_statement(self, statement: str, params=None) -> bool:
        "Usado para Inserções, Deleções, Alter Tables"
        try:
            if params:
                self.cursor.execute(statement, params)
            else:
                self.cursor.execute(statement)

            self.conn.commit()
        except Exception as e:
            print("Erro no execute_statement:", e)
            self.conn.rollback()
            return False
        return True

    def execute_select_all(self, query: str, params=None) -> list[dict[str, Any]]:
        "Usado para SELECTS no geral"
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

        return [dict(item) for item in self.cursor.fetchall()]

    def execute_select_one(self, query: str, params=None) -> dict | None:
        "Usado para SELECT com apenas uma linha de resposta"
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

        query_result = self.cursor.fetchone()

        if not query_result:
            return None

        return dict(query_result)
