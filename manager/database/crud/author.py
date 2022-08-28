from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Author as AuthorModel
from ..schemas.author import AuthorCreate


def create_author(db: Session, author: AuthorCreate) -> AuthorModel | None:
    db_book = AuthorModel(**author.dict())

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_author_by_id(db: Session, author_id: int) -> AuthorModel | None:
    return db.get(AuthorModel, author_id)


def get_authors(db: Session) -> list[AuthorModel] | list:
    return db.scalars(select(AuthorModel)).all()


def get_author_books(db: Session, author_id: int) -> list[AuthorModel] | list:
    author = db.scalar(select(AuthorModel).where(AuthorModel.id == author_id))

    return [author_book.book for author_book in author.books]
