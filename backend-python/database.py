from dotenv import load_dotenv
load_dotenv()
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")
print("🔥 ENV DATABASE_URL:", DATABASE_URL)

if not DATABASE_URL:
    print("❌ NO DATABASE_URL → dùng SQLite")
    DATABASE_URL = "sqlite:///./chat.db"
else:
    print("✅ USING POSTGRES:", DATABASE_URL)

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args=connect_args
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# ✅ QUAN TRỌNG: phải có cái này
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()