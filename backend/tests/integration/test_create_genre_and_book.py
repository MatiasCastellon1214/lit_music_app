def test_create_genre_and_book(client):
    genre = {"name": "Sci-Fi", 
             "description": "Science Fiction"}
    response = client.post("/book_genres/", json=genre)
    assert response.status_code == 201
    genre_id = response.json()["id"]

    book = {"title": "Dune", 
            "author": "Frank Herbert", 
            "genres_id": [genre_id]
            }
    response = client.post("/books/", json=book)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Dune"
    assert data["author"] == "Frank Herbert"
