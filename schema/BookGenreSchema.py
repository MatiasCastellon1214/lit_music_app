def book_genre_schema(book_genre) -> dict:
    return {
        "id": str(book_genre["_id"]),
        "name": str(book_genre["name"]),
        "description": str(book_genre["description"])
    }

def book_genres_schema(book_genres):
    return [book_genre_schema(book_genre) for book_genre in book_genres]