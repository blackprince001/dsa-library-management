from pathlib import Path

from manager.utils.book_metadata_parser import load_metadata

filename = Path(__file__).resolve().parent.parent.parent / 'books.json'


def test_metadata():
    assert load_metadata(filename=filename)[0] == (
        ["blackprince001"],
        "Follow who know Road",
        419,
        "Everyday we face the problem of not being able to accomplish much with what we have. Don't fret, if you read this book, you know the person who know Road. That's all I have for you!",
    )