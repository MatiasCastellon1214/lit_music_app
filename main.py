from fastapi import FastAPI
from routers import user_router, book_router, book_genre_router

app = FastAPI(
    title="Literature Music App",
    version="0.0.1"
)

app.include_router(user_router.router)
app.include_router(book_router.router)
app.include_router(book_genre_router.router)


