
def book_schema(book) -> dict:

    # Get images if they exist
    images = []

    if book.get("image", []):
        if "image" in book and isinstance(book["image"], list):
            image_ids = book["image"]
            # Convertir ObjectId a string para cada imagen
            images = [str(img_id) if isinstance(img_id, object) else img_id for img_id in image_ids]

    return {
        "id": str(book["_id"]),
        "title": book["title"],
        "author": book["author"],
        "genres_id": [str(genre_id) for genre_id in book["genres_id"]],
        "sentiment": book.get("sentiment"),
        "image": images,
        "created_at": book.get("created_at"),
        "updated_at": book.get("updated_at")
    }


def books_schema(books):
    return [book_schema(book) for book in books]