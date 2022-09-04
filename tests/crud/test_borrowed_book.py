from manager.database.crud.borrowed_book import (
    create_borrowed_book,
    remove_borrowed_book,
    get_borrowed_books,
    get_borrowed_books_admin,
)
from manager.database.crud.book import create_book
from manager.database.crud.author import AuthorCreate, create_author
from manager.database.crud.user import create_user
from manager.database.schemas.book import BorrowedBookCreate, BookCreate


def test_create_borrowed_book(db, book, author, user):
    db_author = create_author(db=db, author=author)
    db_user = create_user(db=db, user=user)
    db_book = create_book(db=db, book=book, author_ids=[db_author.id])

    db_borrowed_book = create_borrowed_book(
        db=db, borrow_book=BorrowedBookCreate(user_id=db_user.id, book_id=db_book.id)
    )

    assert db_borrowed_book.book_id == db_book.id
    assert db_borrowed_book.user_id == db_user.id


def test_removed_book():
    pass


def test_borrowed_books():
    pass


def test_borrowed_books_admin():
    pass
