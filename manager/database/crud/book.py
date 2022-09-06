from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import AuthorBook as AuthorBookModel, Book as BookModel
from ..models import Author as AuthorModel
from ..schemas.book import BookCreate


def create_book(
    db: Session,
    book: BookCreate,
    author_ids: list[int],
) -> BookModel:
    """
    Returns a book instance after adding to the database.
        @param `db` - accepts the database Session engine
        @param `book` - a book
        @param `author_ids` - a list of author ids from a the database.
                            do note that before you can create a book, the authors must already exist.
        more at ../tests/crud/test_book.py
    """
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


def get_book_by_id(db: Session, book_id: int) -> BookModel:
    """Returns a book using it's `id`"""
    return db.get(BookModel, book_id)


def get_books(db: Session) -> list[BookModel] | list:
    """Returns a list of all books from the Book Column in the database."""
    return db.scalars(select(BookModel)).all()


def display_book_content(db: Session, book: BookCreate) -> None:
    """Outputs the data of a book."""
    print(f"Book Name: {book.title}\nPages: {book.pagecount}\nBlub: {book.description}")
