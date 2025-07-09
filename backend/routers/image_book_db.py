from fastapi import APIRouter, HTTPException, status, UploadFile, File
from fastapi.params import Form
from db.config import db
from models.image_book.ImageBookModel import ImageBook
from schema.ImageBookSchema import image_book_schema, image_books_schema
from bson import ObjectId

from utils.s3_utils import delete_image_from_aws, upload_image_to_aws


# pip install boto3 python-multipart

router = APIRouter(prefix="/image_bookdb",
                        tags=["image_bookdb"],
                        responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})


def image_search_book(field: str, key):
    try:
        image_book = db.image_books.find_one({field: key})
        print(image_book)
        return ImageBook(**image_book_schema(image_book))
    except:
        return {"error": "Image of book not found"}
    

# GET

@router.get("/", response_model= list[ImageBook])
async def image_books():
    return image_books_schema(db.image_books.find())
    
# Llamada a la imagen de un producto por id - Path  
@router.get("/{id}")
async def image_book(id: str):
    return image_search_book("_id", ObjectId(id))
'''''
# Llamada a la imagen de un libro por id - Query
@router.get("/search")
async def image_book(id: str):
    return image_search_book("_id", ObjectId(id))
'''

# POST
@router.post("/", 
             response_model= ImageBook, 
             status_code= status.HTTP_201_CREATED)
async def create_image_book(file: UploadFile = File(...),
                                book_id: str = Form(...)):
    if not book_id:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, 
            detail="Book ID is required")
    
    if type(image_search_book("image_book", file.filename)) == ImageBook:
        raise HTTPException(
        status.HTTP_404_NOT_FOUND, 
        detail="Image of Book already exists")
    
    # Subir la imagen a AWS S3
    s3_url = upload_image_to_aws(file.file, file.filename, file.content_type)

    image_book_dict = {
        "image_book": s3_url,
        "book_id": book_id
    }

    if not isinstance(s3_url, str) and 'error' in s3_url:
        raise HTTPException(
        status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=s3_url["error"])

    # Crear el objeto de la imagen del libro generada
    #image_book = ImageBook(image=s3_url)

    
    # Insertar la imagen del libro en la base de datos
    id = db.image_books.insert_one(image_book_dict).inserted_id

    # Actualizar la lista de imágenes del libro
    db.books.update_one(
        {"_id": ObjectId(book_id)}, 
        {"$push": {"image": id}})

    new_image_book = image_book_schema(db.image_books.find_one({"_id": id}))

    return ImageBook(**new_image_book)

# PUT
@router.put("/{id}")
async def update_image_book(id: str, file: UploadFile = File(...)):
    image_book = image_search_book("_id", ObjectId(id))
    
    if type(image_book) != ImageBook:
        raise HTTPException(
        status.HTTP_404_NOT_FOUND, 
        detail="Image of Book not found")
    
    # Eliminar la imagen del bucket S3
    current_s3_url = image_book.image_book
    if current_s3_url:
        try:
            delete_image_from_aws(current_s3_url)
        except:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Error deleting image of Product from AWS")
    
    # Subir la nueva imagen a AWS S3
    try:
        s3_url = upload_image_to_aws(file.file, file.filename, file.content_type)
    except:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Error uploading image of Book to AWS")

    image_book_dict = {"image_book": s3_url}

    if not isinstance(s3_url, str) and 'error' in s3_url:
        raise HTTPException(
        status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=s3_url["error"])
    
    # Actualizar la imagen del libro en la base de datos
    db.image_books.update_one({"_id": ObjectId(id)}, {"$set": image_book_dict})

    return ImageBook(**image_book_schema(
        db.image_books.find_one({"_id": ObjectId(id)})))


  
# DELETE
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image_book(id: str):

    try:
        # Buscar la imagen de libro en la base de datos
        image = db.image_books.find_one({"_id": ObjectId(id)})
        if not image:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, 
                detail="Image of Book not found")

        #object_id = ObjectId(id)

        # Eliminar la referencia de la imagen en el libro
        if "book_id" in image:
            db.books.update_one(
                {"_id": ObjectId(image["book_id"])}, 
                {"$pull": {"image": ObjectId(id)}}
            )

        # Eliminar la imagen
        if "image_book" in image:
            delete_image_from_aws(image["image_book"])

        # Eliminar la imagen de libro de la base de datos
        db.image_books.delete_one({"_id": ObjectId(id)})    

        return {"message": "Image of Book deleted successfully"}

    except Exception as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, 
            detail="Invalid ID")
    