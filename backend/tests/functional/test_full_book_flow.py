from backend.utils.s3_utils import delete_image_from_aws

def test_full_book_flow(client):
    # 1. Create genre
    r = client.post("/book_genres/", json={"name": "Horror"})
    assert r.status_code == 201
    genre_id = r.json()["id"]

    # 2. Create book
    book = {"title": "IT", "author": "Stephen King", "genres_id": [genre_id]}
    r = client.post("/books/", json=book)
    assert r.status_code == 201
    book_id = r.json()["id"]

    # 3. Upload real image to S3
    r = client.post(
        "/image_bookdb/",
        files={"file": ("image.jpg", b"fake content", "image/jpeg")},
        data={"book_id": book_id}
    )
    assert r.status_code == 201
    image_url = r.json()["image_book"]

    # 4. Verify that the image was uploaded to the correct bucket
    assert image_url.startswith("https://") and "s3.amazonaws.com" in image_url

    # 5. Delete the image from the bucket
    try:
        delete_image_from_aws(image_url)
        print(f"[INFO] Image deleted successfully: {image_url}")
    except Exception as e:
        print(f"[WARNING] Could not delete image from bucket: {e}")
