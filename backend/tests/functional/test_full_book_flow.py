def test_full_book_flow(client, monkeypatch):
    # 1. Genre
    r = client.post("/book_genres/", json={"name": "Horror"})
    assert r.status_code == 201
    genre_id = r.json()["id"]

    # 2. Book
    book = {"title": "IT", "author": "Stephen King", "genres_id": [genre_id]}
    r = client.post("/books/", json=book)
    assert r.status_code == 201
    book_id = r.json()["id"]

    # 3. Image (mock upload to S3)
    def fake_upload(*args, **kwargs):
        print("FAKE UPLOAD CALLED")
        return "https://mock-bucket.s3.fake/image.jpg"

    monkeypatch.setattr("backend.routers.image_book_db.upload_image_to_aws", fake_upload)


    # ✅ Usar files + data para subir UploadFile correctamente
    r = client.post(
        "/image_bookdb/",
        files={"file": ("image.jpg", b"fake content", "image/jpeg")},
        data={"book_id": book_id}
    )
    assert r.status_code == 201
    assert "https://mock-bucket" in r.json()["image_book"]
