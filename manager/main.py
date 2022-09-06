import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manager.database.crud.author import (
    create_author,
    get_author_books,
    get_author_by_id,
    get_authors,
)
from manager.database.schemas.book import (
    BookCreate,
    BorrowedBookCreate,
    BorrowedBook as BorrowedBookSchema,
)
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
    get_books,
    display_book_content,
    get_book_by_id,
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
from manager.utils.book_metadata_parser import METADATA
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

    if not (
        db.get(AuthorModel, 1)
    ):  # check if there are data elements at the top in each Column of Author Table and Book Table

        # load the list collection of data tuples into @param `books`
        books = METADATA
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
    with Session(engine, autoflush=False, autocommit=False) as session:
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
            authors=get_authors(db=db)
        )

        print("\n", "*" * 30)
        options = "\n".join(
            (
                "1. View available books",
                "2. View borrowed books",
                "3. Borrow a book",
                "4. Return a book",
                "5. Search a book",
                "6. Search an Author",
                "7. Logout",
            )
        )

        print(options)
        choice = input("What to do?: ")

        match choice:
            case "1":  # print all the books in the library
                for ind, book in enumerate(library.books, start=1):
                    print(f"{ind} - {book.title}")

            case "2":  # prints the books borrowed by a user
                print(
                    f"\nThese are the books you have Borrowed:\n{','.join([book.title for book in library.borrowed_books])}"
                )

            case "3":  # borrow a book from the library
                search = input("What is the name of the Book you want Borrow: ")
                books = [book for book in library.books if search in book.title]

                if len(books) == 1:
                    print(f"Found '{books[0].title}' \nBorrowing Book.")
                    create_borrowed_book(
                        db,
                        borrow_book=BorrowedBookCreate(
                            user_id=user.id, book_id=books[0].id
                        ),
                    )
                    print(f"You have borrowed '{books[0].title}'")

                elif len(books) > 1:
                    print("Did you mean this? ")
                    for book in books:
                        print(f"{book.id} - {book.title}")

                    response = int(
                        input(
                            "Type the corresponding id of a book if it is suggested above: "
                        )
                    )
                    create_borrowed_book(
                        db,
                        borrow_book=BorrowedBookCreate(
                            user_id=user.id, book_id=response
                        ),
                    )
                else:
                    print(
                        f"Book Not Found! Are you sure {search} is a book in the library?"
                    )

            case "4":  # return a book to the library
                for book in library.borrowed_books:
                    print(f"{book.id} - {book.title}")

                return_book = int(
                    input(
                        "Which book do you want to return (type the id of the book from the above):"
                    )
                )
                remove_borrowed_book(
                    db=db,
                    borrowed_book=BorrowedBookSchema(
                        book_id=return_book, user_id=user.id
                    ),
                )
                print(f"Book with id {return_book} has been returned!")

            case "5": # Search for a book
                search = input("What book do you want to search for: ")
                results = [book for book in library.books if search in book.title]

                if not results:
                    print(
                        f"Book Not Found! Are you sure {search} is a book in the library?"
                    )

                if results:
                    print(f"Found books with the search '{search}' :\n")
                    for book in results:
                        print(f"id: {book.id} title: {book.title}")

                    response = int(
                        input(
                            "Type the corresponding id of a book if it is suggested above: "
                        )
                    )

                    display_book_content(db, book=get_book_by_id(db, response))

            case "6": # Search up an Author
                search = input("Which Author do you want to search for: ")
                authors = [author for author in library.authors if search in author.name]

                if not authors:
                    print(
                        f"Author Not Found! Are you sure {search} is an Author with books in the library?"
                    )

                if authors:
                    print(f"Found Authors with the search '{search}' :\n")
                    for author in authors:
                        print(f"id: {author.id} title: {author.name}")

                    response = int(
                        input(
                            "Type the corresponding id of an Author if it is suggested above: "
                        )
                    )
                    author = get_author_by_id(db, response)
                    print(f"Author Name: {author.name}")

                    author_books = get_author_books(db, author.id)
                    print(f"Author Books: {','.join([book.title for book in author_books])}")

            case "7":
                show_main_menu()

            case _:
                print("Invalid entry, try again!")


def view_library_as_admin(admin: Admin):
    db = get_db()

    print(f"\nHello, admin: {admin.username}\n")

    while True:

        library = Library(
            admins=get_admins(db=db),
            users=get_users(db=db),
            books=get_books(db=db),
            borrowed_books=get_borrowed_books_admin(db=db),
            authors=get_authors(db=db)
        )

        options = "\n".join(
            (
                "1. Create an admin account",
                "2. View all books",
                "3. View borrowed books",
                "4. View all Authors",
                "5. Logout",
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
                print("\n")

            case "2":
                for book in library.books:
                    print(
                        f"Book Name: {book.title}\nPages: {book.pagecount}\nBlub: {book.description}\n"
                    )

            case "3":
                print(f"{','.join([book.title for book in library.borrowed_books])}")

            case "4":
                authors = {author for author in library.authors}
                for name in authors:
                    print(name)

            case "5":
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


def app():
    d_create_admins()
    d_load_books()
    show_main_menu()
