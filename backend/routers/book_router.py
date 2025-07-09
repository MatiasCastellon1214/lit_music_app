## Book DB API##

from typing import List
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from models.book.BookModel import Book
from models.book.BookCreate import BookCreate
from models.book_genre.BookGenreModel import BookGenre
from schema.BookSchema import book_schema, books_schema
from db.config.db import db
from services.BookService import create_book, delete_book, search_book, update_book


router = APIRouter(prefix="/books", 
                   tags=["books"],
                   responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}}) 


# GET - All Books
@router.get('/', tags=['books'],
            response_model= List[Book])
async def get_books():
    return books_schema(db.books.find())


# GET - Calling a book by id - Path
@router.get('/{id}', tags=['books'],
            response_model=Book)
async def book(id: str):
    return search_book('_id', ObjectId(id))


# POST 
@router.post('/', tags=['books'],
             response_model=Book,
             status_code=status.HTTP_201_CREATED)
async def create_new_book(book: BookCreate):
    return create_book(book)


# PUT
@router.put('/{id}', tags=["books"], 
            response_model=Book)
async def update_existing_book(id: str, book: BookCreate):
    return update_book(id, book)


# DELETE
@router.delete('/{id}', tags=["books"], 
            response_model=Book)
async def remove_book(id: str):
    return delete_book(id)


