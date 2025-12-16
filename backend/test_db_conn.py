#!/usr/bin/env python3
"""Simple DB connectivity test that uses the service's DATABASE_URL env var.

Run as a one-off on Render so it uses the same environment variables:
  python backend/test_db_conn.py

This will print the parsed host/port/db/user and attempt a `SELECT 1`.
"""
import os
import sys
import traceback
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url


def main():
    url = os.getenv("DATABASE_URL")
    if not url:
        print("DATABASE_URL not set in environment")
        sys.exit(1)

    try:
        parsed = make_url(url)
        print(f"Connecting to {parsed.host}:{parsed.port} db={parsed.database} user={parsed.username}")
    except Exception:
        print("Using DATABASE_URL (raw):", url)

    try:
        engine = create_engine(
            url,
            connect_args={"sslmode": "require"},
            pool_pre_ping=True,
            pool_size=1,
            max_overflow=0,
            pool_timeout=10,
        )
        with engine.connect() as conn:
            r = conn.execute(text("SELECT 1")).scalar()
            print("Query result:", r)
        print("Connection test succeeded")
        sys.exit(0)
    except Exception as e:
        print("Connection test failed:")
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()
