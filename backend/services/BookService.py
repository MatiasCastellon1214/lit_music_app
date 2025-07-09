from datetime import datetime
from typing import List
from bson import ObjectId
from fastapi import HTTPException, status
from db.config.db import db
from models.book.BookModel import Book
from schema.BookGenreSchema import book_genre_schema, book_genres_schema
from schema.BookSchema import book_schema
import logging

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Validate if genre exists
def validate_genre_exist(genre_ids: List[str]):
    try:

        for genre_id in genre_ids:
            logger.info(f"Validating genre ID: {genre_id}")

            # Verify if genre_id is a valid ObjectId
            if not ObjectId.is_valid(genre_id):
                logger.error(f"Invalid genre ID format: {genre_id}")

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid genre format"
                )

            # Search for genre in the database
            logger.info(f"Searching for gender with ID: {genre_id}")
            genre = db.book_genres.find_one({"_id": ObjectId(genre_id)})

            if not genre:
                logger.error(f"Genre with id {genre_id} not found")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Genre not found"
                )

            logger.info(f"Genre found: {genre}")
            return genre

    except Exception as e:
        logger.error(f"Error validating gener ID: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Genre id not exists"
        )


# Search Book
def search_book(field: str, key):
    try:
        book = db.books.find_one({field: key})

        if not book:
            return {"error": "Book not found"}
    
        print(book)
        return Book(**book_schema(book))
    except:
        return {"error": "Book not found"}
    


# Create Book
def create_book(book: Book):
    try:
        logger.info(f"Creating book: {book.title}")

        existing_book = search_book('title', book.title)
        if isinstance(existing_book, Book):
            logger.warning(f"Book already exists: {book.title}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Book already exists'
            )

        validate_genre_exist(book.genres_id)

        book_dict = book.model_dump()
        book_dict["genres_id"] = [ObjectId(genre_id) for genre_id in book.genres_id]
        book_dict["created_at"] = datetime.now()

        id = db.books.insert_one(book_dict).inserted_id

        logger.info(f"Book created with ID: {id}")

        new_book = book_schema(db.books.find_one({'_id': id}))

        return Book(**new_book)

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error creating book: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error creating book'
        )


# Update Book
def update_book(id: str, book: Book):
    try:
        logger.info(f"Updating book with ID: {id}")

        if not ObjectId.is_valid(id):
            logger.error(f"Invalid book ID format: {id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid book ID"
            )

        existing_book = db.books.find_one({"_id": ObjectId(id)})
        if not existing_book:
            logger.warning(f"Book not found with ID: {id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Book not found'
            )

        validate_genre_exist(book.genres_id)

        book_dict = book.model_dump(exclude='id')
        book_dict["updated_at"] = datetime.now()

        result = db.books.find_one_and_update(
            {'_id': ObjectId(id)},
            {'$set': book_dict},
            return_document=True
        )

        if result is None:
            logger.warning(f"Book not updated, not found: {id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Book not found'
            )

        logger.info(f"Book updated: {result}")
        return Book(**book_schema(result))

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error updating book: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'An error occurred: {e}'
        )


def delete_book(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid book Id'
        )
    
    book_found = db.books.find_one({'_id': ObjectId(id)})

    if not book_found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    db.books.delete_one({'_id': ObjectId(id)})

    
    return Book(**book_schema(book_found))
