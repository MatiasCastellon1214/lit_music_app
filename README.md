# Lit Music App

## Descripción

Lit Music App es una aplicación que combina música y literatura, permitiendo a los usuarios descubrir libros y canciones relacionadas.

## Requisitos

- Python 3.12 o superior
- MongoDB
- Git

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/MatiasCastellon1214/lit_music_app.git
   ```
2. Instala las dependencias del backend:
   ```bash
   pip install -r requirements.txt
   ```


## Ejecución

Para iniciar la aplicación, ejecuta el siguiente script:

```bash
./run_all.sh
```

Este script se encargará de:

1. Iniciar MongoDB.
2. Entrenar el modelo de Machine Learning.
3. Iniciar el backend de FastAPI con Uvicorn.

Una vez iniciado, podrás acceder a la API en `http://127.0.0.1:8000`.



También puedes hacer correr manualmente en caso de no querer hacer correr el modelo de machine learning:

```bash
cd backend/
```

```bash
uvicorn main:app --reload
```

### Entrenar el modelo de Machine Learning

Desde root:

```bash
cd machine_learning/scripts/

python -m train_models
```

### Tests

Desde root:

```bash
cd backend/tests/
```

Por ejemplo, para hacer correr la prueba unitaria:

```bash
pytest -v unit/test_models.py 
```

### Docs

En la carpeta **docs**, ubicada en root, se encuentra documentación de funcionamiento.