import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manager.database.crud.author import create_author
from manager.database.schemas.book import BookCreate, BorrowedBookCreate
from manager.database.schemas.author import AuthorCreate
from manager.security import Password
from manager.database.schemas.users import (
    Admin,
    AdminCreate,
    UserCreate,
    User as UserSchema,
)
from manager.database.schemas.library import Library
from manager.database.crud.book import (
    create_book,
    get_book_by_name,
    get_books,
    display_book_content,
)
from manager.database.models import (
    Base,
    Book as BookModel,
    User as UserModel,
    Author as AuthorModel,
)
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
from manager.utils.book_metadata_parser import load_metadata
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
    "elom": "admin3",
    "emmanuel": "admin4",
    "henry": "admin5",
    "joshua": "admin6",
    "jesse": "admin7",
    "aidoo": "admin8",
}


def d_create_admins():
    db = get_db()

    # check if there are data elements in User Column before adding them
    if not db.scalars(select(UserModel).where(UserModel.is_admin == True)).all():
        for admin, password in GROUP_MEMBERS.items():
            create_user(db=db, user=AdminCreate(username=admin, password=password))


def d_load_books():
    db = get_db()
    print("LOADING SYSTEM")
    # assigns the path location for the books.json to @var raw_file
    raw_file = Path(__file__).resolve().parent.parent / "books.json"

    # load the list collection of data tuples into @param `books`
    books = load_metadata(raw_file)

    if not (
        db.get(AuthorModel, 1)
    ):  # check if there are data elements at the top in each Column of Author Table and Book Table

        for (authors, title, page_count, desc) in books:
            # unpack the tuples to and create Authors and Books.

            create_book(
                db=db,
                book=BookCreate(title=title, pagecount=page_count, description=desc),
                author_ids=[
                    author.id
                    for author in [
                        create_author(db=db, author=AuthorCreate(name=writer))
                        for writer in authors
                    ]
                ],
            )


# snippet ends here!


def get_db():
    with Session(engine) as session:
        return session


def view_library(user: UserSchema):
    db = get_db()

    print(f"\nHello, user: {user.username}\n")

    while True:
        library = Library(
            admins=[],
            users=[],
            books=get_books(db=db),
            borrowed_books=get_borrowed_books(db=db, user_id=user.id),
        )

        print("\n", "*" * 30)
        options = "\n".join(
            (
                "1. View available books",
                "2. View borrowed books",
                "3. Borrow a book",
                "4. Return a book",
                "5. Read a book",
                "6. Logout",
            )
        )

        print(options)
        choice = input("What to do?: ")

        match choice:
            case "1":  # print all the books in the library
                for book in library.books:
                    print(book.title)

            case "2":  # prints the books by a user
                print(
                    f"\nThese are the books you have Borrowed:\n{library.borrowed_books}"
                )

            case "3":  # borrow a book from the library
                search = input("What is the name of the Book you want Borrow: ")
                res = get_book_by_name(db=db, keyword=search)

                if res:
                    create_borrowed_book(
                        db,
                        borrow_book=BorrowedBookCreate(user_id=user.id),
                        book_id=res[0].id,
                    )
                    print(f"You have borrowed '{search}'")
                else:
                    print(f"Are you sure this '{search}' is a book?")

            case "4":  # return a book to the library
                borrowed = library.borrowed_books
                for book in borrowed:
                    print(f"{book.id} - {book.title}")

                return_book = int(
                    input(
                        "Which book do you want to return (type the id of the book from the above):"
                    )
                )
                remove_borrowed_book(
                    db=db,
                    borrowed_book=BorrowedBookCreate(
                        user_id=user.id, book_id=return_book
                    ),
                )
                print(f"Book with id {return_book} has been returned!")

            case "5":  # display book blub
                books = library.books

                # this section might break if the search keyword is not worded right, but I didnt have the time to error check.
                search = input("What is the name of the book: ")
                book_found = None
                for book in books:
                    if book.title == search:
                        book_found = book

                print("\n\n")
                display_book_content(db=db, book=book_found)

            # case "6":
            #     search = input("What book do you want to search for: ")
            #     res = get_book_by_name(db, keyword=search)

            #     if not res:
            #         print

            #     if res:
            #         print(f"Found books with the search '{search}' :\n")
            #         for count, book in enumerate(res, start=1):
            #             print(f"{count} - {book}")

            case "6":
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

    d_create_admins()
    d_load_books()
    show_main_menu()
