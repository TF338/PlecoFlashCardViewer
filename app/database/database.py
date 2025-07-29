import os
import shutil
from pathlib import Path
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR}/database/chineseDict.db"
EXPORT_DIR = BASE_DIR / "database_export"

# Create engine without model dependency
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=None
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session_factory = scoped_session(SessionLocal)

def init_db(create_tables=False):
    """
    Initialize database from latest .pqb backup or create new.
    Set create_tables=True if you want to initialize empty tables.
    """
    # Ensure directories exist
    (BASE_DIR / "database").mkdir(parents=True, exist_ok=True)
    db_file = BASE_DIR / "database" / "chineseDict.db"

    if db_file.exists():
        print("Database already exists, skipping initialization")
        return

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Find most recent .pqb file
    pqb_files = sorted(
        EXPORT_DIR.glob("*.pqb"),
        key=os.path.getmtime,
        reverse=True
    )

    if pqb_files:
        latest_pqb = pqb_files[0]
        print(f"Initializing database from backup: {latest_pqb.name}")

        # Copy backup to database location
        shutil.copy2(
            latest_pqb,
            BASE_DIR / "database" / "chineseDict.db"
        )

        # Verify the database is valid
        try:
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            print("Database initialized successfully")
        except Exception as e:
            print(f"Invalid database file: {e}")
            if create_tables:
                _create_empty_database()
    elif create_tables:
        _create_empty_database()
    else:
        print("No database backup found and create_tables=False")


def _create_empty_database():
    """Create a brand new empty database"""
    print("Creating new empty database")
    metadata = MetaData()
    metadata.create_all(engine)
    print("Empty database created")


@contextmanager
def get_sync_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# === FastAPI Dependency ===
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()