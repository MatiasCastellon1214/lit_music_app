
def book_schema(book) -> dict:


    return {
        "id": str(book["_id"]),
        "title": book["title"],
        "author": book["author"],
        "genres_id": [str(genre_id) for genre_id in book["genres_id"]],
        "created_at": book.get("created_at"),
        "updated_at": book.get("updated_at")
    }


def books_schema(books):
    return [book_schema(book) for book in books]