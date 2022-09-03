from manager.database.crud.borrowed_book import (
    create_borrowed_book,
    remove_borrowed_book,
    get_borrowed_books,
    get_borrowed_books_admin,
)
from manager.database.crud.book import create_book
from manager.database.crud.author import AuthorCreate, create_author
from manager.database.schemas.book import BorrowedBookCreate, BookCreate

def test_create_borrowed_book(db, book):
    author = create_author(
        db=db,
        author=AuthorCreate(name='King Sark'),
    )

    db_book = create_book(db=db, book=book, author_ids=[author.id])

    db_borrowed_book = create_borrowed_book(db, db_book)

    assert db_borrowed_book.user_id == book.id


def test_removed_book():
    pass

def test_borrowed_books():
    pass

def test_borrowed_books_admin():
    pass