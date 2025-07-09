
import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv(".env.test")


try:
    client = MongoClient("mongodb://localhost:27017/")

    if os.getenv("MONGO_DB_TEST") == "true":
        db = client.lit_music_app_test  # <--- Base de test
        print("✅ Connected to TEST database!")
    else:
        db = client.lit_music_app  # <--- Base normal
        print("✅ Connected to LOCAL database!")

    books = db["books"]
    comments = db["comments"]
    image_books = db["image_books"]
    book_genres = db["book_genres"]

except Exception as e:
    print(f"❌ Connection error: {e}")
"""
# Remote Database
#db_client = MongoClient(
#   'mongodb+srv://test:test@cluster0.q9a4d.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0').test
"""



'''

from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv
import os
'''
'''
# Local Database
try:
    engine = create_engine('mysql+pymysql://root:1214@localhost:3306/storedb')

    meta = MetaData()

    conn = engine.connect()
    print("✅ Succeful connection to the local database")
except Exception as e:
    print(f"❌ Connection error: {e}")

'''
'''
# Remote Database
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Verificar si la variable de entorno está cargada correctamente
if not DATABASE_URL:
    raise ValueError("❌ No se encontró la variable DATABASE_URL en .env")



try:
    engine = create_engine(DATABASE_URL)
    
    meta = MetaData()

    conn = engine.connect()
    print("✅ Succeful connection to the remote database")
except Exception as e:
    print(f"❌ Connection error: {e}")
'''