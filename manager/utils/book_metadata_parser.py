import json
from pathlib import Path

def load_metadata(filename):
    """Returns a list collection of tuples packed with scraped data from a filename."""
    books = list()

    with open(filename, "r") as file:
        data = json.load(file)  # loads data into data variable

        for packet in data:
            if not (
                "longDescription" in packet.keys()
            ):  # check if a specific packet has a longDescription Key
                books.append(
                    (
                        packet["authors"],
                        packet["title"],
                        packet["pageCount"],
                        "No description for this book at the moment!",
                    )
                )
                continue

            # adds books to collection.
            books.append(
                (
                    packet["authors"],
                    packet["title"],
                    packet["pageCount"],
                    packet["longDescription"],
                )
            )

    return books


# assigns the path location for the books.json to @var raw_file
raw_file = Path(__file__).resolve().parent.parent.parent / "books.json"
METADATA = load_metadata(raw_file)