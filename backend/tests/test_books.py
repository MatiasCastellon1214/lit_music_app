def test_create_genre_and_book(client):
    # 1. Create a genre
    genre_data = {"name": "Fantasy",
                  "description": "Fantasy books"
                  }
    response = client.post("/book_genres/", json=genre_data)
    assert response.status_code == 201
    genre_id = response.json()["id"]

    # 2. Create a book with the created genre
    book_data = {
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "genres_id": [genre_id]
        }
    response = client.post("/books/", json=book_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "The Hobbit"
    assert data["author"] == "J.R.R. Tolkien"
