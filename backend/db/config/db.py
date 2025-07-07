# Módulo conexión MongoDB: pip install pymongo
# Ejecución: sudo mongod --dbpath "/path/a/la/base/de/datos/"
# mongod --dbpath "C:\Users\Mirty\Documents\lit_music_app\db"
# Conexión: mongodb://localhost

from pymongo import MongoClient

try:
    # Local Database
    db_client = MongoClient("mongodb://localhost:27017/").lit_music_app
    print("✅ Succeful connection to the local database")
except Exception as e:
    print(f"❌ Connection error: {e}")

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
    print(f"❌ Connection error: {e}")'''