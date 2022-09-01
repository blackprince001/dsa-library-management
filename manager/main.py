import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manager.security import Password
from manager.database.schemas.users import (
    Admin,
    AdminCreate,
    UserCreate,
    User as UserSchema,
)
from manager.database.schemas.library import Library
from manager.database.crud.book import (
    get_book_by_name,
    get_books
)
from manager.database.models import Base, User as UserModel
from manager.database.crud.user import (
    create_user,
    get_admins,
    get_user_by_username,
    get_users,
)
from manager.database.crud.borrowed_book import (
    create_borrowed_book,
    remove_borrowed_book,
    get_borrowed_books,
    get_borrowed_books_admin,
)
from manager.database.core import engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from getpass import getpass

Base.metadata.create_all(bind=engine)

# For Group Project Demonstration purposes

GROUP_MEMBERS = {
    "prince": "admin1",
    "richard": "admin2",
    "elorm": "admin3",
    "emmanuel": "admin4",
    "henry": "admin5",
    "joshua": "admin6",
}


def d_create_default_admins():
    db = get_db()

    if not db.scalars(select(UserModel).where(UserModel.is_admin == True)).all():
        for admin, password in GROUP_MEMBERS.items():
            create_user(db=db, user=AdminCreate(username=admin, password=password))


# snippet ends here!


def get_db():
    with Session(engine) as session:
        return session


def view_library(user: UserSchema):
    db = get_db()

    library = Library(
        admins=[],
        users=get_users(db=db),
        books=get_books(db=db),
    )

    print(f"\nHello, user: {user.username}\n")

    while True:

        print("\n", "*" * 30)
        options = "\n".join(
            (
                "1. View available books",
                "2. View borrowed books",
                "3. Borrow a book",
                "4. Return a book",
                "5. Logout",
            )
        )

        print(options)
        choice = input("What to do?: ")

        match choice:
            case "1":
                print(f"\nLoading Book Catalog:\n{library.books}")
            case "2":
                print(
                    f"\nThese are the books you have Borrowed:\n{user.borrowed_books}"
                )
            case "3":
                title = input("What is the title of the book you wish to borrow? ")
                # to be completed soon
            case "4":
                print("... Not implemented...")
            case "5":
                show_main_menu()
            case _:
                print("Invalid entry, try again!")


def view_library_as_admin(admin: Admin):
    db = get_db()

    library = Library(
        admins=get_admins(db=db),
        users=get_users(db=db),
        books=get_books(db=db),
        borrowed_books=get_borrowed_books_admin(db=db),
    )

    print(f"\nHello, admin: {admin.username}\n")

    while True:

        options = "\n".join(
            (
                "1. Create an admin account",
                "2. View all books",
                "3. View borrowed books",
                "4. Logout",
            )
        )

        print(options)
        choice = input("What to do?: ")

        match choice:
            case "1":
                username = input("\nUsername: ")
                password = getpass()

                if password != getpass("\nRepeat password: "):
                    print("Passwords do not match")
                    view_library_as_admin()

                create_user(
                    db=db, user=AdminCreate(username=username, password=password)
                )
            case "2":
                print(f"\nLoading Book Catalog:\n{library.books}")
            case "3":
                print(f"\nThese books have been Borrowed:\n{library.borrowed_books}")
            case "4":
                show_main_menu()
            case _:
                print("Invalid entry, try again!")


def login():
    print("\nLogging in\n")
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
                    password=password,
                ),
            )
        except IntegrityError:
            print("Username already registered")
            sys.exit()

        print("Account created successfully")

    login()


def show_main_menu():
    print("\nWelcome")

    while True:

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
                show_main_menu()


if __name__ == "__main__":

    d_create_default_admins()

    show_main_menu()
