from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import (
    BorrowedBook as BorrowedBookModel,
    User as UserModel,
)
from ..schemas.book import BookCreate, BorrowedBookCreate


def create_borrowed_book(db: Session, book: BookCreate) -> BorrowedBookModel:
    """Creates a book and adds the Book to the BorrowedBook Table Database."""
    db_borrowed_book = BorrowedBookModel(**book.dict())

    db.add(db_borrowed_book)
    db.commit()
    db.refresh()

    return db_borrowed_book


def remove_borrowed_book(db: Session, borrowed_book: BorrowedBookCreate) -> None:
    """Removes a current book from BorrowedBook Table Database."""
    db_borrowed_book = db.get(BorrowedBookModel, borrowed_book.book_id)

    db.delete(db_borrowed_book)
    db.commit()
    db.refresh()

    print(f"{db_borrowed_book} has been removed from borrowed books.")


def get_borrowed_books_admin(db: Session) -> list[BorrowedBookModel] | list:
    """Returns a list of books borrowed from the library."""
    return db.scalars(
        select(BorrowedBookModel).where(BorrowedBookModel is not None)
    ).all()


def get_user_by_id(db: Session, user_id: int) -> UserModel | None:
    """Gets a user by the user_id."""
    return db.get(UserModel, user_id)


def get_borrowed_books(db: Session, user_id: int):
    """Returns a list of books borrowed by a specific User."""
    user = get_user_by_id(db, user_id)

    if user is None:
        raise Exception("User not found!")

    return [borrowed_book.book for borrowed_book in user.borrowed_books]
