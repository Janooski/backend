import os
from collections.abc import Generator

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

postgres_url = f"postgresql+psycopg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
engine = create_engine(postgres_url, echo=True)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

def drop_tables() -> None:
    SQLModel.metadata.drop_all(engine)

def get_session() -> Generator[Session, any]:
    with Session(engine) as session:
        yield session
