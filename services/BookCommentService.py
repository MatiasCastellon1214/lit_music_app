from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status
from db.config.db import db_client
from models.book_comment.BookCommentModel import BookComment
from schema.BookCommentSchema import book_comment_schema, book_comments_schema
import logging


# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_book_exists(book_id: str):
    try:
        logger.info(f"Validating book ID: {book_id}")

        # Verify if the book_id is a valid ObjectId
        if not ObjectId.is_valid(book_id):
            logger.error(f"Invalid book ID format: {book_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid book ID format"
            )
    
        # Search for book in the databse
        logger.info(f"Searching for book with ID: {book_id}")
        book = db_client.books.find_one({"_id": ObjectId(book_id)})

        if not book:
            logger.error(f"Book with ID {book_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        
        logger.info(f"Book found: {book}")
        return book

    except Exception as e:
        logger.error(f"Error validating book ID: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Book id not exists"
        )
    

    
def search_book_comment(field: str, key):
    try:
        book_comment = db_client.book_comments.find_one({field: key})

        if not book_comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book comment not found"
            )
        
        return BookComment(**book_comment_schema(book_comment))
    except Exception as e:
        logger.error(f"Error searching book comment: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while searching for the book comment"
        )



def create_book_comment(book_comment: BookComment):
    try:
        # Verify if book id exists before create comment
        validate_book_exists(book_comment.book_id)

        # Convert comment to a dict
        book_comment_dict = book_comment.model_dump()

        # Automatically add creation date
        book_comment_dict["created_at"] = datetime.now()

        # Insert book comment into database
        id = db_client.book_comments.insert_one(book_comment_dict).inserted_id

        # Obtain comment recentrly created
        new_book_comment = book_comment_schema(db_client.book_comments.find_one({"_id": id}))

        return BookComment(**new_book_comment)
    
    except HTTPException as e:
        # Captur validation excepcions and release
        raise e
    except Exception as e:
        logger.error(f"Error creating book comment: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the book comment"
        )
    
def update_book_comment(comment_id: str, update_book_comment: BookComment):

    if not ObjectId().is_valid(comment_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book comment not found"
        )
    
    existing_book_comment = db_client.book_comments.find_one({"_id": ObjectId(comment_id)}) 

    if not existing_book_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    # Verify if book id exists before create comment
    validate_book_exists(update_book_comment.book_id)
    
    book_comment_dict = update_book_comment.model_dump(exclude={"created_at", "updated_at"})

    book_comment_dict["updated_at"] = datetime.now()

    try:
        result = db_client.book_comments.find_one_and_update(
            {"_id": ObjectId(comment_id)},
            {"$set": book_comment_dict},
            return_document=True
        )

        if result is None:
            logger.error(f"Book comment with id={comment_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book comment not found"
            )
        
        return BookComment(**book_comment_schema(result))
    
    except Exception as e:
        logger.error(f"Error updating book comment: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the book comment"
        )


def delete_book_comment(id: str):

    # Validate if the ID is a valid ObjectId
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail='Invalid book genre Id'
        )
    

    book_comment_found = db_client.book_comments.find_one({"_id": ObjectId(id)})

    if not book_comment_found:
        logger.error(f"Book comment with id={id} not found")
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book comment not found"
        )
       
            
    db_client.book_comments.delete_one({"_id": ObjectId(id)})

    return book_comment_found
        

def get_comment_for_book(book_id: str):

    try:
        comments = db_client.book_comments.find({"book_id": book_id})
        return book_comments_schema(comments)
    except Exception as e:
        logger.error(f"Error getting comments for book: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while getting comments for book"
        )