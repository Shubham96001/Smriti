from collections.abc import Callable, Iterable, Iterator
from typing import Any

from psycopg import Connection
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from config import settings

pool = ConnectionPool(
    conninfo=settings.database_url,
    kwargs={"row_factory": dict_row},
    open=False,
    min_size=1,
    max_size=10,
)


def open_pool() -> None:
    pool.open()


def close_pool() -> None:
    if not pool.closed:
        pool.close()


def get_connection() -> Iterator[Connection[Any]]:
    with pool.connection() as connection:
        yield connection


def fetch_one(query: str, params: Iterable[Any] | None = None) -> dict[str, Any] | None:
    with pool.connection() as connection, connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchone()


def fetch_all(query: str, params: Iterable[Any] | None = None) -> list[dict[str, Any]]:
    with pool.connection() as connection, connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()


def execute_query(query: str, params: Iterable[Any] | None = None) -> int:
    with pool.connection() as connection, connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.rowcount


def execute_returning(query: str, params: Iterable[Any] | None = None) -> dict[str, Any] | None:
    with pool.connection() as connection, connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchone()


def execute_transaction(operation: Callable[[Connection[Any]], Any]) -> Any:
    with pool.connection() as connection:
        with connection.transaction():
            return operation(connection)


def check_connection() -> bool:
    try:
        return fetch_one("SELECT 1 AS ready") is not None
    except Exception:
        return False