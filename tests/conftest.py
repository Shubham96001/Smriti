import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from uuid import uuid4

import httpx
import pytest

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from config import get_settings


def _test_connection_details() -> tuple[dict[str, str], str]:
    try:
        from psycopg.conninfo import conninfo_to_dict, make_conninfo
    except ModuleNotFoundError:
        pytest.skip("Install backend requirements to run PostgreSQL integration tests")
    settings = get_settings()
    details = conninfo_to_dict(settings.database_url)
    host = details.get("host", "localhost")
    if host not in {"localhost", "127.0.0.1", "::1"}:
        pytest.skip("Integration fixtures only create databases on loopback PostgreSQL")
    database_name = details.get("dbname", "postgres")
    test_name = f"{database_name}_test"
    admin_details = {**details, "dbname": details.get("maintenance_db", "postgres")}
    return admin_details, make_conninfo(**{**details, "dbname": test_name})


@pytest.fixture(scope="session")
def test_database():
    import psycopg
    from psycopg.conninfo import conninfo_to_dict, make_conninfo
    from psycopg import sql

    admin_details, test_url = _test_connection_details()
    database_name = conninfo_to_dict(test_url)["dbname"]
    try:
        with psycopg.connect(make_conninfo(**admin_details), autocommit=True) as connection:
            connection.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name)))
    except psycopg.errors.DuplicateDatabase:
        pytest.skip(f"Test database {database_name} already exists; refusing to modify it")
    except psycopg.Error as error:
        pytest.skip(f"Local PostgreSQL is unavailable: {error.__class__.__name__}")

    environment = os.environ.copy()
    environment["DATABASE_URL"] = test_url
    environment["PYTHONPATH"] = str(BACKEND)
    try:
        subprocess.run(
            [sys.executable, "sql/run_migrations.py"],
            cwd=BACKEND,
            env=environment,
            check=True,
        )
        yield test_url
    finally:
        with psycopg.connect(make_conninfo(**admin_details), autocommit=True) as connection:
            connection.execute(
                "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = %s AND pid <> pg_backend_pid()",
                (database_name,),
            )
            connection.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(database_name)))


@pytest.fixture(scope="session")
def base_url(test_database):
    import uvicorn

    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    environment = os.environ.copy()
    environment["DATABASE_URL"] = test_database
    environment["PYTHONPATH"] = str(BACKEND)
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", str(port)],
        cwd=BACKEND,
        env=environment,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    url = f"http://127.0.0.1:{port}"
    try:
        for _ in range(100):
            if process.poll() is not None:
                pytest.fail("Uvicorn exited before becoming healthy")
            try:
                if httpx.get(f"{url}/api/health", timeout=0.5).status_code == 200:
                    break
            except httpx.HTTPError:
                time.sleep(0.1)
        else:
            pytest.fail("Uvicorn did not become healthy")
        yield url
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


@pytest.fixture
def api(base_url):
    with httpx.Client(base_url=base_url, timeout=10) as client:
        yield client


def register(client: httpx.Client, role: str = "patient") -> dict:
    unique = uuid4().hex
    response = client.post(
        "/api/auth/register",
        json={
            "email": f"{role}-{unique}@example.com",
            "password": "correct horse battery staple",
            "full_name": f"Test {role.title()}",
            "role": role,
            "consent_acknowledged": True,
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


@pytest.fixture
def patient(api):
    return register(api, "patient")


@pytest.fixture
def caregiver(api):
    return register(api, "caregiver")


@pytest.fixture
def hcw(api):
    return register(api, "hcw")


def auth_headers(account: dict) -> dict[str, str]:
    return {"Authorization": f"Bearer {account['access_token']}"}