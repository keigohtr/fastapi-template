from typing import Generator

import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from app.config import Config
from app.db.base import Base
from app.logger import logger
from app.services.book_service import BookService
from tests.db.session import build_uri, get_engine


def get_database_name(worker_id):
    return f"test_database_{worker_id}"


def create_test_engine(worker_id):
    return get_engine(get_database_name(worker_id))


def configure_test_book_service() -> BookService:
    return BookService(config=Config.initialize_from_env())


@pytest.fixture
def create_testing_session_local():  # pylint: disable=missing-function-docstring
    def TestingSessionLocal(worker_id):
        return sessionmaker(autocommit=False, autoflush=False, bind=create_test_engine(worker_id))()

    return TestingSessionLocal


@pytest.fixture(scope="function")
def function_db(worker_id, create_testing_session_local) -> Generator:  # pylint: disable=missing-function-docstring
    session = create_testing_session_local(worker_id)
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def session_db(worker_id, create_testing_session_local) -> Generator:
    session = create_testing_session_local(worker_id)
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(autouse=True, scope="function")
def setup_db(worker_id):
    logger.info("Initializing test DB")
    url = build_uri(get_database_name(worker_id))
    if not database_exists(url):
        create_database(url)
    Base.metadata.drop_all(bind=create_test_engine(worker_id))
    Base.metadata.create_all(bind=create_test_engine(worker_id))
    logger.info("finished initializing")
    yield


@pytest.fixture
def book_service():
    return configure_test_book_service()
