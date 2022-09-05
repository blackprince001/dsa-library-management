from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import (
    BorrowedBook as BorrowedBookModel,
    BorrowedBook as BorrowedBookSchema,
    User as UserModel,
)
from ..schemas.book import BorrowedBookCreate


def create_borrowed_book(
    db: Session, borrow_book: BorrowedBookCreate
) -> BorrowedBookModel:
    """Creates a borrowed book and records the Book to the BorrowedBook Table Database."""
    db_borrowed_book = BorrowedBookModel(**borrow_book.dict())

    db.add(db_borrowed_book)
    db.commit()
    db.refresh(db_borrowed_book)

    return db_borrowed_book


def remove_borrowed_book(db: Session, borrowed_book: BorrowedBookSchema) -> None:
    """Removes a current book from BorrowedBook Table Database."""
    db_borrowed_book = db.scalar(
        select(BorrowedBookModel)
        .where(BorrowedBookModel.book_id == borrowed_book.book_id)
        .where(BorrowedBookModel.user_id == borrowed_book.user_id)
    )

    db.delete(db_borrowed_book)
    db.commit()


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
