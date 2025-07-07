#!/bin/bash

echo "📦 Iniciando MongoDB..."
mongod &

sleep 5  # Le damos un poco de tiempo a MongoDB para que se inicie

echo "🧠 Entrenando modelo de Machine Learning..."
cd machine_learning/scripts
python -m train_models

echo "🚀 Iniciando backend FastAPI con Uvicorn..."
cd ../../backend
uvicorn main:app --reload
