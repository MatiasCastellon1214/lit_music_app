import os
import joblib

from machine_learning.scripts.data_prep import clean_text


# Ruta absoluta a este archivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Subir un nivel a /machine_learning
MODEL_DIR = os.path.join(BASE_DIR, '..', 'models')

# Rutas absolutas del modelo y vectorizador
MODEL_PATH = os.path.abspath(os.path.join(MODEL_DIR, 'best_model.pkl'))
VECTORIZER_PATH = os.path.abspath(os.path.join(MODEL_DIR, 'vectorizer.pkl'))

# Cargar modelo y vectorizador
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

def predict_sentiment(text: str) -> str:
    print("[DEBUG] Ejecutando predict_sentiment actualizado")
    cleaned = clean_text(text)
    X = vectorizer.transform([cleaned])
    X_dense = X.toarray()
    prediction = model.predict(X_dense)[0]
    print("[DEBUG] Ejecutando predict_sentiment actualizado")
    return "positive" if prediction == 1 else "negative"
