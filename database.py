# database.py — Repositório: toda interação com o SQLite fica aqui

import sqlite3
from config import DB_PATH


class CandidaturaRepository:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self._criar_tabela()

    # DB iniciador
    def _criar_tabela(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS candidaturas (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                empresa         TEXT    NOT NULL,
                cargo           TEXT    NOT NULL,
                link            TEXT,
                data_cadastro   TEXT    NOT NULL,
                status          TEXT    DEFAULT 'Pendente',
                observacoes     TEXT
            )
        ''')
        self.conn.commit()

    def fechar(self):
        """Fecha a conexão com o banco de dados."""
        self.conn.close()

    # CRUD
    def inserir(self, empresa: str, cargo: str, link: str,
                data: str, status: str, obs: str) -> None:
        self.cursor.execute('''
            INSERT INTO candidaturas (empresa, cargo, link, data_cadastro, status, observacoes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (empresa, cargo, link, data, status, obs))
        self.conn.commit()

    def listar_todas(self) -> list[tuple]:
        self.cursor.execute(
            'SELECT * FROM candidaturas ORDER BY data_cadastro DESC'
        )
        return self.cursor.fetchall()