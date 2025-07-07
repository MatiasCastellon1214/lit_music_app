from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status
from db.config.db import db_client
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

        book_genre = db_client.book_genres.find_one({field: key})
        
        if not book_genre:
            return None
        print(book_genre)
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

        if type(search_book_genre('name', book_genre.name)) == BookGenre:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, 
                detail= 'Book genre already exists'
            )
        
        book_genre_dict = book_genre.model_dump()

        book_genre_dict["created_at"] = datetime.now()
        
        id = db_client.book_genres.insert_one(book_genre_dict).inserted_id

        new_book_genre = book_genre_schema(db_client.book_genres.find_one({"_id": id}))

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

    # Validate if Id is a valid ObjectId
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if the book genre exists before updating
    existing_book_genre = db_client.book_genres.find_one({"_id": ObjectId(id)})
    if not existing_book_genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book genre not found"
        )
    
    # Convert Id to ObjectId
    book_genre_dict = book_genre.model_dump()

    book_genre_dict["updated_at"] = datetime.now()

    try:

        result = db_client.book_genres.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": book_genre_dict},
            return_document=True
        )

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book genre not found"
            )
        
        return BookGenre(**book_genre_schema(result))
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error ocurred: {e}"
        )
    

# Delete Book genre
def delete_book_genre(id: str):

    # Validate if the ID is a valid ObjectId
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail='Invalid book genre Id'
        )
    
    book_genre_found = db_client.book_genres.find_one({"_id": ObjectId(id)})

    if not book_genre_found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book genre not found"
        )

    db_client.book_genres.delete_one({"_id": ObjectId(id)})

    return book_genre_found



# Get books by genre
def get_books_by_genre(genre_id: str):

    try:
        if not ObjectId.is_valid(genre_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid genre ID"
            )
        genre = db_client.book_genres.find_one({"_id": ObjectId(genre_id)})
        if not genre:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Genre not found"
            )
        books = db_client.books.find({"genres_id": ObjectId(genre_id)})
        if not books:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No books found for this genre"
            )
        
        return books_schema(books)
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error getting books by genre: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while getting books by genre"
        )
