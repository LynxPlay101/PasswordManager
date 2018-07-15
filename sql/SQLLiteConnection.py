import sqlite3
from inspect import Attribute
from sqlite3 import Connection


class SQLLiteConnection:
    connection: sqlite3.Connection
    file: str

    def __init__(self, file: str):
        self.file = file
        self.connection = None

    def get(self) -> Connection:
        if self.connection is None:
            self.build_connection()
        return self.connection

    def build_connection(self):
        self.connection = sqlite3.connect(self.file)
        pass

    def offer(self, connection: Connection):
        connection.commit()
        connection.close()
        self.connection = None
        pass

    pass
