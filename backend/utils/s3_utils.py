# Establecemos las variables de entorno para conectarnos con AWS S3 fastapi-book-images
# conda env config vars set AWS_ACCESS_KEY_ID="tu_access_key_id"
# conda env config vars set AWS_SECRET_ACCESS_KEY="tu_secret_access_key"
# conda env config vars set AWS_S3_BUCKET="fastapi-book-images"
# Luego desactivar y volver a activar el entorno para que los cambios surtan efecto.

# Instalamos Boto3
# pip install boto3

import os
import boto3
from botocore.exceptions import NoCredentialsError
import uuid
from fastapi import HTTPException

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")


# ✅ Subir imagen a AWS S3
def upload_image_to_aws(file, filename: str, content_type: str):
    s3 = boto3.client("s3")
    try:
        unique_filename = f"{uuid.uuid4()}_{filename}"

        s3.upload_fileobj(
            file,
            AWS_S3_BUCKET,
            unique_filename,
            ExtraArgs={"ContentType": content_type},
        )

        url = f"https://{AWS_S3_BUCKET}.s3.amazonaws.com/{unique_filename}"
        return url

    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading image: {str(e)}")


# ✅ Eliminar imagen de AWS S3
def delete_image_from_aws(s3_url: str):
    s3 = boto3.client("s3")

    if not s3_url.startswith(f"https://{AWS_S3_BUCKET}.s3.amazonaws.com/"):
        raise HTTPException(status_code=400, detail="Invalid URL")

    bucket_key = s3_url.replace(f"https://{AWS_S3_BUCKET}.s3.amazonaws.com/", "")

    try:
        s3.delete_object(Bucket=AWS_S3_BUCKET, Key=bucket_key)
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting image: {str(e)}")


# ✅ Función auxiliar semántica (opcional)
def delete_image_book_from_aws(s3_url: str):
    return delete_image_from_aws(s3_url)
