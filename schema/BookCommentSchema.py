def book_comment_schema(book_comment) -> dict:

    return {
        "id": str(book_comment["_id"]),
        "content": book_comment["content"],
        "book_id": str(book_comment["book_id"]),
        "created_at": book_comment.get("created_at"),
        "updated_at": book_comment.get("updated_at")

    }

def book_comments_schema(book_comments):
    return [book_comment_schema(book_comment) for book_comment in book_comments ]