from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class AuthorBook(Base):
    __tablename__ = "author_book"

    author_id = Column(ForeignKey("author.id"), primary_key=True)
    book_id = Column(ForeignKey("book.id"), primary_key=True)

    book = relationship("Book", back_populates="authors", lazy="selectin")
    author = relationship("Author", back_populates="books", lazy="selectin")


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    books: list[AuthorBook] = relationship(
        "AuthorBook", back_populates="author", lazy="selectin"
    )

    def __repr__(self):
        return (
            f"Author(id={self.id!r}, "
            f"first_name={self.first_name!r}, "
            f"last_name={self.last_name!r})"
        )


class BorrowedBook(Base):
    __tablename__ = "borrowed_book"

    id = Column(Integer, primary_key=True)
    book_id = Column(ForeignKey("book.id"), primary_key=True)
    user_id = Column(ForeignKey("user.id"), primary_key=True)

    book = relationship("Book", back_populates="borrowed_by", lazy="selectin")
    user = relationship("User", back_populates="borrowed_books", lazy="selectin")


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)

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
            f"Book(id={self.id!r}, "
            f"title={self.title!r}), "
            f"authors={[author_book.author for author_book in self.authors]}"
        )


class User(Base):
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
