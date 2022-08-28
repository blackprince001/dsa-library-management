from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import AuthorBook as AuthorBookModel, Book as BookModel
from ..models import Author as AuthorModel
from ..schemas.book import BookCreate


def create_book(db: Session, book: BookCreate, author_ids: list[int]) -> BookModel:
    authors = set()

    for author_id in author_ids:
        author = db.get(AuthorModel, author_id)

        if author is None:
            raise ValueError(f"Author with id {author_id} not found")

        a = AuthorBookModel()
        a.author = author
        authors.add(a)

    db_book = BookModel(**book.dict())

    for author_book in authors:
        db_book.authors.append(author_book)

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_books(db: Session) -> list[BookModel]:
    return db.scalars(select(BookModel)).all()
