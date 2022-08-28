from manager.database.crud.author import (
    create_author,
    get_author_by_id,
    get_authors,
    get_author_books,
)


def test_create_author(db, author):
    db_author = create_author(db=db, author=author)

    assert db_author.first_name == author.first_name
    assert db_author.id == 1


def test_get_author_by_id(db, author):
    db_author = get_author_by_id(db=db, author_id=1)

    assert db_author is not None

    assert db_author.first_name == author.first_name


def test_get_authors(db):
    authors = get_authors(db=db)

    assert len(authors) > 0


def test_get_author_books(db):

    assert get_author_books(db, author_id=1) == []
