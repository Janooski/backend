from collections.abc import Iterator, Generator
from typing import Annotated, Any

import pytest
from fastapi import Depends, Request
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from app.database import create_db_and_tables, drop_tables, get_session
from app.main import app
from app.middlewares.auth_middleware import auth_dependency
from app.services.user_service import create_user, get_user_by_clerk_id


CLERK_ID = "test_clerk_id"


async def override_auth_dependency(request: Request, session: Annotated[Session, Depends(get_session)]) -> Request:
    try:
        create_user(CLERK_ID, "test@email.com", session)
        user = get_user_by_clerk_id("test_clerk_id", session)
    # The bad db test case requires catching the OperationalError in the auth_dependency to correctly return the HTTP code 500
    except OperationalError as _:
        user = None
    request.state.user = user
    return request


def override_get_session() -> Generator[Session, Any, None]:
    engine = create_engine("sqlite:///:memory:")
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)

    db = session()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def db_session() -> Iterator[None]:
    create_db_and_tables()
    yield
    drop_tables()


@pytest.fixture(autouse=True)
def overwrite_auth_dependency() -> Iterator[None]:
    app.dependency_overrides[auth_dependency] = override_auth_dependency
    yield
    app.dependency_overrides[auth_dependency] = auth_dependency


@pytest.fixture()
def overwrite_session_dependency() -> Iterator[None]:
    app.dependency_overrides[get_session] = override_get_session
    yield
    app.dependency_overrides[get_session] = get_session


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)
