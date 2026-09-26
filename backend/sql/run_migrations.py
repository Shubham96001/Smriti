from pathlib import Path
import sys

import psycopg

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import settings


def run_migrations() -> None:
    migration_dir = Path(__file__).resolve().parent
    with psycopg.connect(settings.database_url) as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS schema_migrations "
            "(version TEXT PRIMARY KEY, applied_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP)"
        )
        applied = {
            row[0]
            for row in connection.execute("SELECT version FROM schema_migrations").fetchall()
        }
        for migration_path in sorted(migration_dir.glob("[0-9][0-9][0-9]_*.sql")):
            if migration_path.name in applied:
                continue
            sql = migration_path.read_text(encoding="utf-8")
            with connection.transaction():
                connection.execute(sql)
                connection.execute(
                    "INSERT INTO schema_migrations (version) VALUES (%s)",
                    (migration_path.name,),
                )
            print(f"Applied {migration_path.name}")


if __name__ == "__main__":
    run_migrations()