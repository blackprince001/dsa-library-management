import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from manager.database.models import Base
from manager.database.schemas.author import AuthorCreate
from manager.database.schemas.book import BookCreate


@pytest.fixture(scope="session")
def engine():
    return create_engine(url="sqlite+pysqlite:///:memory:", future=True)


@pytest.fixture(scope="session")
def author():
    return AuthorCreate(first_name="King", last_name="Phyte")


@pytest.fixture(scope="session")
def book():
    return BookCreate(title="The Lone Wolf")


@pytest.fixture
def db(engine):
    with Session(engine) as session:
        Base.metadata.create_all(bind=engine)
        yield session
