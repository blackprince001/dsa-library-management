from pydantic import BaseModel

from manager.database.schemas.book import Book as BookSchema


class UserBase(BaseModel):
    username: str


class StudentCreate(UserBase):
    password: str


class Student(UserBase):
    borrowed_books: list = []

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    def borrow_book(self, book: BookSchema):
        self.borrowed_books.append(book)

    def return_book(self, book: BookSchema):
        self.borrowed_books.remove(book)


class AdminCreate(StudentCreate):
    is_admin: bool = True


class Admin(UserBase):
    is_admin: bool = True

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
