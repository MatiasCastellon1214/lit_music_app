import os
import joblib
from machine_learning.scripts.data_prep import clean_text  # Reutilizás tu limpieza

# Cargar modelo y vectorizer
MODEL_PATH = os.path.join("..", "machine_learning", "models", "best_model.pkl")
VECTORIZER_PATH = os.path.join("..", "machine_learning", "models", "vectorizer.pkl")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

def predict_sentiment(text: str) -> str:
    cleaned = clean_text(text)
    X = vectorizer.transform([cleaned])
    X_dense = X.toarray()  # <-- Aquí convertís a matriz densa
    prediction = model.predict(X_dense)[0]
    return "positive" if prediction == 1 else "negative"
