import json


def load_metadata(filename):
    books = list()

    with open(filename, "r") as file:
        data = json.load(file)

        for packet in data:
            if not ("longDescription" in packet.keys()):
                books.append(
                    (
                        packet["authors"],
                        packet["title"],
                        packet["pageCount"],
                        "No description for this book at the moment!",
                    )
                )
                continue

            books.append(
                (
                    packet["authors"],
                    packet["title"],
                    packet["pageCount"],
                    packet["longDescription"],
                )
            )

    return books
