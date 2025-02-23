
def book_schema(book) -> dict:


    return {
        "id": str(book["_id"]),
        "title": book["title"],
        "author": book["author"],
        "genres": book.get("genres", [])
    }


def books_schema(books):
    return [book_schema(book) for book in books]