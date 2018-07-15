from typing import List, Optional

from sql.ManagedPassword import ManagedPassword
from sql.SQLLiteConnection import SQLLiteConnection
import PasswordCypher as pC
import sql.ManagedPassword as mP


class ManagedPasswordDao:
    connection_pool: SQLLiteConnection
    password_cache = {}

    def __init__(self, connection_pool: SQLLiteConnection):
        self.connection_pool = connection_pool
        pass

    def store(self, entry: ManagedPassword):
        cache = self.lookup_cache(entry.url)
        if cache is not None and entry.equals(cache):
            pass

        self.password_cache[entry.url] = entry

        connection = self.connection_pool.get()

        cursor = connection.cursor()
        cursor.execute('INSERT OR REPLACE INTO passwords VALUES (?,?,?)',
                       [entry.url, pC.encode(entry.username), pC.encode(entry.password)])

        self.connection_pool.offer(connection)
        pass

    def create_table(self):
        connection = self.connection_pool.get()

        cursor = connection.cursor()
        cursor.execute((
            "CREATE TABLE IF NOT EXISTS passwords (url VARCHAR(255), username BLOB, password BLOB,"
            "PRIMARY KEY(url))"
        ))

        self.connection_pool.offer(connection)
        pass

    def all(self) -> List[ManagedPassword]:
        connection = self.connection_pool.get()

        c = connection.cursor()
        c.execute('SELECT * FROM passwords')
        result = list(mP.new_decoded(x[0], x[1], x[2]) for x in c.fetchall())

        self.connection_pool.offer(connection)

        for x in result:
            self.password_cache[x.url] = x
        return result

    def get_force(self, url: str) -> Optional[ManagedPassword]:
        connection = self.connection_pool.get()

        c = connection.cursor()
        c.execute('SELECT * FROM passwords WHERE url= ?', [url])

        query = c.fetchone()
        if query is None:
            return None

        result = mP.new_decoded(query[0], query[1], query[2])

        self.connection_pool.offer(connection)
        self.password_cache[url] = result
        return result

    def get(self, url: str) -> Optional[ManagedPassword]:
        p = self.lookup_cache(url)
        if p is None:
            p = self.get_force(url)
        return p

    def lookup_cache(self, url: str) -> ManagedPassword:
        return self.password_cache.get(url)

    def get_cache(self) -> List[ManagedPassword]:
        result = []
        for x in self.password_cache.values():
            result.append(x)
        return result

    pass

    def remove(self, url):
        del self.password_cache[url]

        connection = self.connection_pool.get()

        c = connection.cursor()
        c.execute("DELETE FROM passwords WHERE url=?", (url,))

        self.connection_pool.offer(connection)
        pass
