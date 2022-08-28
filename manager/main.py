from getpass import getpass

import sys

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from manager.database.core import engine
from manager.database.crud.user import (
    create_user,
    get_admins,
    get_user_by_username,
    get_users,
)
from manager.database.models import Base
from manager.database.crud.book import get_books
from manager.database.schemas.library import Library
from manager.database.schemas.users import (
    Admin,
    AdminCreate,
    UserCreate,
    User as UserSchema,
)

from manager.security import Password


Base.metadata.create_all(bind=engine)


def get_db():
    with Session(engine) as session:
        return session


def view_library(user: UserSchema):
    db = get_db()

    library = Library(
        admins=get_admins(db=db),
        users=get_users(db=db),
        books=get_books(db=db),
    )

    print(f"Hello, user: {user.username}")

    options = "\n".join(
        (
            "1. View available books",
            "2. View borrowed books",
            "3. Borrow a book",
            "4. Return a book",
        )
    )

    print(options)
    choice = input("What to do?: ")

    match choice:
        case "1":
            print(library.books)
        case "2":
            print(user.borrowed_books)
        case "3":
            print("... Not implemented...")
        case "4":
            print("... Not implemented...")
        case _:
            print("Invalid entry")


def view_library_as_admin(admin: Admin):
    db = get_db()

    library = Library(
        admins=get_admins(db=db),
        users=get_users(db=db),
        books=get_books(db=db),
    )

    print(f"Hello, admin {admin.username}")

    options = "\n".join(
        (
            "1. Create an admin account",
            "2. View all books",
            "3. View borrowed books",
        )
    )

    print(options)

    choice = input("What to do?: ")

    match choice:
        case "1":
            username = input("Username: ")
            password = getpass()

            if password != getpass("Repeat password: "):
                print("Passwords do not match")
                sys.exit()

            create_user(db=db, user=AdminCreate(username=username, password=password))
        case "2":
            print(library.books)
        case "3":
            print(library.borrowed_books)
        case _:
            print("Invalid entry")


def login():
    print("Logging in")
    username = input("Username: ")
    password = getpass()

    user = get_user_by_username(db=get_db(), username=username)

    print(user)
    if user is None:
        print("Incorrect username or password")
        return

    if not Password.verify(password, user.password):
        print("Incorrect username or password")
        return

    if user.is_admin:
        return view_library_as_admin(user)

    return view_library(user)


def sign_up():
    username = input("Username: ")
    password = getpass()

    if password != getpass("Repeat password: "):
        print("Passwords do not match")
        sys.exit()

    with Session(engine) as db:
        try:
            create_user(
                db=db,
                user=UserCreate(
                    username=username,
                    password=Password.hash(password),
                ),
            )
        except IntegrityError:
            print("Username already registered")

        print("Account created successfully")

    login()


def show_main_menu():
    print("Welcome")

    options = "\n".join(
        (
            "1. Log in",
            "2. Sign up",
            "3. Quit",
        )
    )
    print(options)
    choice = input("What to do?: ")

    match choice:
        case "1":
            login()
        case "2":
            sign_up()
        case "3":
            sys.exit()
        case _:
            print("Invalid entry")
            sys.exit()


if __name__ == "__main__":
    show_main_menu()
