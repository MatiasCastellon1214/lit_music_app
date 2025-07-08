from fastapi import FastAPI
from routers import image_book_db
from routers import user_router, book_router, book_genre_router, book_comment_router
from dotenv import load_dotenv
load_dotenv() 

print("Starting Literature Music App..")


app = FastAPI(
    title="Literature Music App",
    version="0.0.1"
)

@app.get("/")
def read_root():
    return {"Message": "Literature Music App is Running now"}

app.include_router(user_router.router)
app.include_router(book_router.router)
app.include_router(book_genre_router.router)
app.include_router(book_comment_router.router)
app.include_router(image_book_db.router)


