from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class AuthorBook(Base):
    """
    An Author Book relational Table that binds an `Author` Table to a `Book` Table using ids.
    This has a pattern for many-to-many relationships between data Models.
    It has a `author_id` column, and a `book_id` column.
    """

    __tablename__ = "author_book"

    author_id = Column(ForeignKey("author.id"), primary_key=True)
    book_id = Column(ForeignKey("book.id"), primary_key=True)

    book = relationship("Book", back_populates="authors", lazy="selectin")
    author = relationship("Author", back_populates="books", lazy="selectin")


class Author(Base):
    """
    An Author Model Table that has an `id` column, a `name` column, and has a list of related `books`.
    It has a one-to-many relationship with the `Author Book` Table.
    """

    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    books: list[AuthorBook] = relationship(
        "AuthorBook", back_populates="author", lazy="selectin"
    )

    def __repr__(self):
        return f"Author(id={self.id!r}" f"name={self.name!r}"


class BorrowedBook(Base):
    """
    A Borrowed Book relational Table that binds a `User` Table to a `Book` Table using ids.
    This has common pattern for many-to-many relationships between data Models.
    It has a `user_id` column, and a `book_id` column.
    """

    __tablename__ = "borrowed_book"

    id = Column(Integer, primary_key=True)
    book_id = Column(ForeignKey("book.id"), primary_key=True)
    user_id = Column(ForeignKey("user.id"), primary_key=True)

    book = relationship("Book", back_populates="borrowed_by", lazy="selectin")
    user = relationship("User", back_populates="borrowed_books", lazy="selectin")


class Book(Base):
    """
    A Book Table that has a one-to-many relationship with `Borrowed Book` Table and `Authors` Table.
    It has an `id` column, a `title` column, a `pagecount` column, and a `description` column.
    """

    __tablename__ = "book"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    pagecount = Column(Integer, nullable=False)
    description = Column(String, nullable=False)

    authors: list[AuthorBook] = relationship(
        "AuthorBook",
        back_populates="book",
        lazy="selectin",
    )

    borrowed_by: list[BorrowedBook] = relationship(
        "BorrowedBook",
        back_populates="book",
        lazy="selectin",
    )

    def __repr__(self):
        return (
            f"Book(id={self.id!r}\n"
            f"title={self.title!r})\n "
            f"pageCount={self.pagecount!r}\n "
            f"description={self.description!r}\n "
            f"authors={[print(author_book.author + ',') for author_book in self.authors]}"
        )


class User(Base):
    """
    A User Table that has an `id` column, a `username` column, a `password` and `is_admin` columns.
    It has a one-to-one relationship with `Borrowed Book` Table.
    """

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    is_admin = Column(Boolean, nullable=False, default=False)

    borrowed_books: list[BorrowedBook] = relationship(
        "BorrowedBook", back_populates="user", lazy="selectin"
    )

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, is_admin={self.is_admin!r})"
