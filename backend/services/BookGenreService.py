from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status
from db.config.db import db
from models.book_genre.BookGenreModel import BookGenre
from schema.BookGenreSchema import book_genre_schema
import logging

from schema.BookSchema import books_schema


# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# Search Book genre
def search_book_genre(field:str, key):

    try:
        logger.info(f"Searching book genre with {field}={key}")
        book_genre = db.book_genres.find_one({field: key})
        
        if not book_genre:
            logger.info(f"No book genre found for {field}={key}")
            return None
        logger.info(f"Book genre found: {book_genre}")
        return BookGenre(**book_genre_schema(book_genre))
    
    except Exception as e:
        logger.error(f"Error searching book genre: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while searching for the book genre"
        )
    


# Create book genre
def create_book_genre(book_genre: BookGenre):
    try:

        logger.info(f"Creating book genre: {book_genre.name}")
        if type(search_book_genre('name', book_genre.name)) == BookGenre:

            logger.warning(f"Book genre already exists: {book_genre.name}")
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, 
                detail= 'Book genre already exists'
            )
        
        book_genre_dict = book_genre.model_dump()

        book_genre_dict["created_at"] = datetime.now()
        
        id = db.book_genres.insert_one(book_genre_dict).inserted_id
        logger.info(f"Book genre created with ID: {id}")

        new_book_genre = book_genre_schema(db.book_genres.find_one({"_id": id}))

        return BookGenre(**new_book_genre)

    except HTTPException as e:
        # Captur validation excepcions and release
        raise e
    except Exception as e:
        logger.error(f"Error creating book genre: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the book genre"
        )


# Update Book genre
def update_book_genre(id: str, book_genre: BookGenre):
    logger.info(f"Updating book genre with ID: {id}")

    # Validate if Id is a valid ObjectId
    if not ObjectId.is_valid(id):
        logger.error(f"Invalid book genre ID: {id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if the book genre exists before updating
    existing_book_genre = db.book_genres.find_one({"_id": ObjectId(id)})
    if not existing_book_genre:
        logger.warning(f"Book genre not found with ID: {id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book genre not found"
        )
    
    # Convert Id to ObjectId
    book_genre_dict = book_genre.model_dump()

    book_genre_dict["updated_at"] = datetime.now()

    try:

        result = db.book_genres.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": book_genre_dict},
            return_document=True
        )

        if result is None:
            logger.warning(f"Book genre not updated; not found: {id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book genre not found"
            )
        
        logger.info(f"Book genre updated: {result}")
        return BookGenre(**book_genre_schema(result))
    
    except Exception as e:
        logger.exception(f"Error updating book genre: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error ocurred: {e}"
        )
    

# Delete Book genre
def delete_book_genre(id: str):
    logger.info(f"Deleting book genre with ID: {id}")

    # Validate if the ID is a valid ObjectId
    if not ObjectId.is_valid(id):
        logger.error(f"Invalid book genre ID: {id}")
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail='Invalid book genre Id'
        )
    
    book_genre_found = db.book_genres.find_one({"_id": ObjectId(id)})

    if not book_genre_found:
        logger.warning(f"Book genre not found with ID: {id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book genre not found"
        )

    db.book_genres.delete_one({"_id": ObjectId(id)})
    logger.info(f"Book genre deleted: {book_genre_found}")

    return book_genre_found



# Get books by genre
def get_books_by_genre(genre_id: str):

    try:
        logger.info(f"Getting books for genre ID: {genre_id}")
        if not ObjectId.is_valid(genre_id):
            logger.error(f"Invalid genre ID: {genre_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid genre ID"
            )
        genre = db.book_genres.find_one({"_id": ObjectId(genre_id)})
        if not genre:
            logger.warning(f"Genre not found: {genre_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Genre not found"
            )
        
        books = db.books.find({"genres_id": ObjectId(genre_id)})
        books_list = list(books)

        if not books:
            logger.info(f"No books found for genre ID: {genre_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No books found for this genre"
            )
        
        logger.info(f"Found {len(books_list)} books for genre ID: {genre_id}")
        return books_schema(books_list)
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error getting books by genre: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while getting books by genre"
        )
