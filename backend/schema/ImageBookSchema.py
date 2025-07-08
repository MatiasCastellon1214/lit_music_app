from bson import ObjectId

def image_book_schema(image_book) -> dict:
    if isinstance(image_book, ObjectId):
        # Si recibimos un ObjectId, solo devolvemos un string
        return str(image_book)
    
    """
    Convierte un documento de imagen de libro en un diccionario con claves estandarizadas.
    """
    return {
        "id": str(image_book["_id"]),
        "image_book": image_book["image_book"],
        "book_id": str(image_book["book_id"] if "book_id" in image_book else "") 
    }

def image_books_schema(image_books) -> list:

    if not image_books:
        return []

    """
    Convierte una lista de documentos de imágenes de productos en una lista de diccionarios.
    """
    # Si es una lusta de ObjectId, convertirlas directamente
    if isinstance(image_books, ObjectId):
        return [str(image_book) for image_book in image_books]

    return [image_book_schema(image_book) for image_book in image_books]