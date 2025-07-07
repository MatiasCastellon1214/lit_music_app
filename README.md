# 📚 Lit Music App

Aplicación que combina análisis de sentimientos con reseñas de libros, utilizando Machine Learning, FastAPI y MongoDB.

---

## 🧠 Requisitos

Asegurate de tener instalados:

- Python 3.12
- MongoDB (instalado localmente y accesible mediante `mongod`)
- Git + Git LFS
- Entorno virtual configurado (`venv`, `conda`, etc.)

Instala las dependencias ejecutando:

```bash
pip install -r requirements.txt
```

> 📦 Si usás `nltk`, asegurate de ejecutar también:

```python
import nltk
nltk.download('punkt')
```

---

## 📁 Estructura del proyecto

```
lit_music_app/
│
├── backend/                  # API REST con FastAPI
│   ├── main.py               # Punto de entrada del servidor
│   └── ...                   # Routers, servicios, modelos, etc.
│
├── machine_learning/
│   ├── data/                 # Datasets (uno pesado está en .gitignore)
│   ├── models/               # Modelos finales entrenados (vectorizer + modelo)
│   ├── scripts/              # Scripts para entrenamiento e inferencia
│   └── notebooks/            # Exploración y análisis
│
├── requirements.txt
├── run_all.sh               # Script para ejecutar todo
└── README.md
```

---

## 🚀 ¿Cómo ejecutar el proyecto?

Desde la raíz del proyecto, simplemente ejecutá:

```bash
bash run_all.sh
```

Este script:

1. Inicia MongoDB (`mongod`)
2. Entrena el modelo (si es necesario)
3. Levanta el backend con FastAPI

Accedé a la documentación Swagger:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📝 Notas

- El archivo `Books_rating.csv` es muy pesado (~2.7 GB), por lo tanto **no está en el repositorio**. Si lo necesitas, descargalo desde [Kaggle](https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews) y ubicalo en `machine_learning/data/`.
- Las rutas de los modelos entrenados se encuentran en:`machine_learning/models/best_model.pkl``machine_learning/models/vectorizer.pkl`
- Evitá la carpeta `machine_learning/machine_learning/models/`, puede eliminarse si está duplicada.

---

## 👨‍💻 Autor

Matías Castellón
Proyecto desarrollado como parte de la formación en programación y análisis de datos.
