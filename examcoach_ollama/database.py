"""
database.py — SQLAlchemy only, Supabase Session Pooler.
Connection is lazy (first request), not at import time.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set.\n"
        "Check your .env file — get the exact URL from:\n"
        "  Supabase Dashboard → Project Settings → Database → Session pooler"
    )

# pool_pre_ping tests the connection before using it from the pool
# connect_args sslmode=require is needed for Supabase
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"sslmode": "require"},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    """FastAPI dependency — yields a SQLAlchemy session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_connection():
    """Call this to test the DB connection and print a clear result."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection FAILED: {e}")
        print("\nFix: Open .env and confirm DATABASE_URL matches exactly what")
        print("Supabase shows at: Dashboard → Settings → Database → Session pooler")
        return False
