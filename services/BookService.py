from bson import ObjectId
from fastapi import HTTPException, status
from db.config.db import db_client
from models.BookModel import Book
from schema.BookGenreSchema import book_genre_schema
from schema.BookSchema import book_schema


# Search Book
def search_book(field: str, key):
    try:
        book = db_client.books.find_one({field: key})

        if not book:
            return {"error": "Nook not found"}
    
        print(book)
        return Book(**book_schema(book))
    except:
        return {"error": "Book not found"}
    


# Create Book
def create_book(book: Book):

    if type(search_book('title', book.title)) == Book:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, 
            detail= 'Book already exists'
        )



    book_dict = book.model_dump()

    id = db_client.books.insert_one(book_dict).inserted_id

    new_book = book_schema(db_client.books.find_one({'_id': id}))

    return Book(**new_book)


# Update Book
def update_book(id: str, book: Book):

    
    # Validate if the Id is a valid ObjectId
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )
    # Check if the book exists before updating
    existing_book = db_client.books.find_one({"_id": ObjectId(id)})
    if not existing_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )
    
    # Convert Id to ObjectId
    book_dict = book.model_dump(exclude='id')
    
    try:

        result = db_client.books.find_one_and_update(
            {'_id': ObjectId(id)},
            {'$set': book_dict},
            return_document=True
        )

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= 'Book not found'
            )
        
        return Book(**book_schema(result))

    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'An error ocurred: {e}'
        )
    

# Delete Book
def delete_book(id: str):

    # Validate if the ID is a valid ObjectId
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail='Invalid book Id'
        )
    
    book_found = db_client.books.find_one({'_id': ObjectId(id)})

    if not book_found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    db_client.books.delete_one({'_id': ObjectId(id)})

    return book_found
