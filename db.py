import contextlib
import sqlite3
from typing import Generator


class Pool:
    def __init__(self, filename: str, pool_size: int):
        self.filename = filename
        self.pool_size = pool_size
        self.connection_pool = self.make_connections(
            filename=filename, pool_size=pool_size
        )

    def make_connections(
        self, filename: str, pool_size: int
    ) -> list[sqlite3.Connection]:
        pool = []
        for _ in range(pool_size):
            connection = sqlite3.connect(filename, check_same_thread=False)
            pool.append(connection)
        return pool

    def aquire(self) -> sqlite3.Connection:
        if len(self.connection_pool) == 0:
            return sqlite3.connect(self.filename)
        return self.connection_pool.pop()

    def release(self, connection):
        if len(self.connection_pool) < 5:
            self.connection_pool.append(connection)


class DB:
    def __init__(self, filename: str, pool_size: int = 5):
        self.filename = filename
        self.connection_pool = Pool(filename=filename, pool_size=pool_size)

    @contextlib.contextmanager
    def get_cursor(self) -> Generator[sqlite3.Cursor, None, None]:
        connection = self.connection_pool.aquire()
        cursor = connection.cursor()
        try:
            yield cursor
        finally:
            connection.commit()
            cursor.close()
            self.connection_pool.release(connection)
