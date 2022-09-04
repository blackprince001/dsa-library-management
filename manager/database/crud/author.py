from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Author as AuthorModel
from ..schemas.author import AuthorCreate


def create_author(db: Session, author: AuthorCreate) -> AuthorModel | None:
    """Creates an Author and adds Author to Author Table Database."""
    db_author = AuthorModel(**author.dict())

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_author_by_id(db: Session, author_id: int) -> AuthorModel | None:
    """Gets a user with a specific id."""
    return db.get(AuthorModel, author_id)


def get_authors(db: Session) -> list[AuthorModel] | list:
    """Returns all authors in the Author Table Database."""
    return db.scalars(select(AuthorModel)).all()


def get_author_books(db: Session, author_id: int) -> list[AuthorModel] | list:
    """Returns all books written or co-authored by a specific author with known id."""
    author = db.scalar(select(AuthorModel).where(AuthorModel.id == author_id))

    return [author_book.book for author_book in author.books]
