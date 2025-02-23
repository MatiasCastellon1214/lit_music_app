def book_genre_schema(book_genre) -> dict:
    return {
        "id": str(book_genre["_id"]),
        "name": str(book_genre["name"]),
        "description": str(book_genre["description"]),
        "created_at": book_genre.get("created_at"),
        "updated_at": book_genre.get("updated_at")
    }

def book_genres_schema(book_genres):
    return [book_genre_schema(book_genre) for book_genre in book_genres]