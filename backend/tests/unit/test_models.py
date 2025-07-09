from pydantic import ValidationError
from models.book.BookCreate import BookCreate
from backend.models.book_genre.BookGenreCreate import BookGenreCreate



def test_book_create_validation():
    try:
        BookCreate(title="Test Book", author="Author", genres_id=[])
    except ValidationError as e:
        errs = e.errors()
        assert errs[0]["type"] == "too_short"
        assert errs[0]["loc"] == ("genres_id",)

def test_genre_create_validation_missing_description():
    try:
        BookGenreCreate(name="Fantasy books")
    except ValidationError as e:
        errs = e.errors()
        assert errs[0]["loc"] == ("description",)


