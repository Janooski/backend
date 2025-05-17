import os
from collections.abc import Generator
from typing import Any

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

postgres_url = f"postgresql+psycopg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
engine = create_engine(postgres_url, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def drop_tables() -> None:
    SQLModel.metadata.drop_all(engine)


def get_session() -> Generator[Session, Any, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
