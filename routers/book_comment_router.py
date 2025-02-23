from typing import List
from bson import ObjectId
from fastapi import APIRouter, status
from models.BookCommentCreate import BookCommentCreate
from schema.BookCommentSchema import book_comment_schema, book_comments_schema
from schema.BookGenreSchema import book_genre_schema
from db.config.db import db_client
from services.BookCommentService import search_book_comment, create_book_comment, update_book_comment, delete_book_comment, get_comment_for_book

from models.BookCommentModel import BookComment

router = APIRouter(prefix="/book_comments",
                    tags=["book_comments"],
                    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}})


# GET - All book comments
@router.get("/", tags=["book_comments"],
             response_model= List[BookComment])
async def get_book_comments():
    return book_comments_schema(db_client.book_comments.find())


# GET - Calling a book comment by id - Path
@router.get("/{id}", tags=["book_comments"],
             response_model= BookComment)
async def get_book_comment(id: str):
    return search_book_comment("_id", ObjectId(id))


# POST
@router.post("/", tags=["book_comments"],
             response_model=BookComment)
async def create_new_book_comment(book_comment: BookCommentCreate):
    return create_book_comment(book_comment)


# PUT
@router.put("/{id}", tags=["book_comments"],
            response_model=BookComment)
async def update_existing_book_comment(id: str, book_comment: BookCommentCreate):
    return update_book_comment(id, book_comment)


# DELETE
@router.delete("/{id}", tags=["book_comments"],
            response_model=BookComment)
async def delete_existing_book_comment(id: str):
    return delete_book_comment(id)


# GET - Get comment by book
@router.get("/book_comments/{book_id}/comments", tags=["book_comments"],
            response_model=List[BookComment])
async def get_comments_for_book_endpoint(book_id: str):
    return get_comment_for_book(book_id)