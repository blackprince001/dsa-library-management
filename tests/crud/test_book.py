from manager.database.crud.author import (
    create_author,
    get_author_books,
)
from manager.database.crud.book import create_book, get_books
from manager.database.schemas.author import AuthorCreate


def test_create_book(db, book):
    first = create_author(
        db=db,
        author=AuthorCreate(
            first_name="King",
            last_name="Phyte",
        ),
    )
    second = create_author(
        db=db,
        author=AuthorCreate(
            first_name="Black",
            last_name="Prince",
        ),
    )

    db_book = create_book(db=db, book=book, author_ids=[first.id, second.id])

    authors = []

    for author_book in db_book.authors:
        authors.append(author_book.author)

    assert (first in authors) and (second in authors)


def test_get_books(db, book):
    books = get_books(db)

    assert books
    assert books[0].title == book.title


def test_get_author_books(db, book, author):
    books = get_author_books(db=db, author_id=2)

    assert len(books) > 0

    db_book = books[0]

    assert db_book.title == book.title
