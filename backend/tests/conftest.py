import sys
import os

# Add the project root to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pytest
# pip install pytest httpx
from fastapi.testclient import TestClient
from backend.main import app
from db.config.db import db, books, comments, image_books, book_genres

@pytest.fixture(scope="session")
def client():
    """
    Fixture for the test client
    """
    return TestClient(app)

@pytest.fixture(autouse=True)
def clean_collections():
    """
    Clean the collections before each test with error handling.
    """
    collections = [
        db["books"],
        db["comments"],
        db["book_genres"],
        db["image_books"]
    ]
    
    # Clean before test (optional, depende de tus necesidades)
    for collection in collections:
        collection.delete_many({})
    
    yield
    
    # Clean after test
    try:
        for collection in collections:
            collection.delete_many({})
    except Exception as e:
        pytest.fail(f"Failed to clean collections: {str(e)}")
