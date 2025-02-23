from typing import List
from fastapi import APIRouter, status
from bson import ObjectId
from db.config.db import db_client
from models.book.BookModel import Book
from models.book_genre.BookGenreCreate import BookGenreCreate
from models.book_genre.BookGenreModel import BookGenre
from schema.BookGenreSchema import book_genres_schema
from services.BookGenreService import create_book_genre, get_books_by_genre, search_book_genre, delete_book_genre, update_book_genre


router = APIRouter(prefix="/book_genres",
                   tags=['book_genres'],
                   responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}})



# GET - All book genres
@router.get("/", tags=["book_genres"],
           response_model=List[BookGenre])
async def get_book_genre():
    return book_genres_schema(db_client.book_genres.find())


# GET - Calling a book genre by id - Path
@router.get("/{id}", tags=["book_genres"],
           response_model=BookGenre)
async def get_book_genre(id: str):
    return search_book_genre("_id", ObjectId(id))


# POST
@router.post("/", tags=["book_genres"],
            response_model=BookGenre)
async def create_new_book_genre(book_genre: BookGenreCreate):
    return create_book_genre(book_genre)


# PUT
@router.put("/{id}", tags=["book_genres"],
            response_model=BookGenre)
async def update_existing_book_genre(id: str, book_genre: BookGenreCreate):
    return update_book_genre(id, book_genre)


# DELETE
@router.delete("/{id}", tags=["book_genres"],
            response_model=BookGenre)
async def delete_existing_book_genre(id: str):
    return delete_book_genre(id)


# GET - Books by genre ID
@router.get("/{genre_id}/books", tags=["book_genres"],
            response_model=List[Book])
async def get_books_by_genre_endpoint(genre_id: str):
    return get_books_by_genre(genre_id)