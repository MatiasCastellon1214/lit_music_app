from bson import ObjectId
from fastapi import HTTPException, status
from db.config.db import db_client
from models.BookCommentModel import BookComment
from models.BookGenreModel import BookGenre
from schema.BookCommentSchema import book_comment_schema
from schema.BookGenreSchema import book_genre_schema





# Search Book genre
def search_book_genre(field:str, key):

    try:
        book_genre = db_client.book_genres.find_one({field: key})
        print(book_genre)
        return BookGenre(**book_genre_schema(book_genre))
    
    except:
        return {"error": "Book genre not found"}
    


# Create book genre
def create_book_genre(book_genre: BookGenre):


    if type(search_book_genre('name', book_genre.name)) == BookGenre:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, 
            detail= 'Book genre already exists'
        )
    
    book_genre_dict = book_genre.model_dump()
    
    id = db_client.book_genres.insert_one(book_genre_dict).inserted_id

    new_book_genre = book_genre_schema(db_client.book_genres.find_one({"_id": id}))

    return BookGenre(**new_book_genre)



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