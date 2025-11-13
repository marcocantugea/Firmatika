import dotenv
import os
from google.cloud import storage
from datetime import timedelta


dotenv.load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GCS_CREDENTIALS_PATH")

def subir_pdf_a_gcs(document_id: str, contenido: bytes) -> str:
    client = storage.Client()
    bucket = client.bucket(os.getenv("GCS_BUCKET_NAME"))
    blob = bucket.blob(f"documentos/{document_id}.pdf")
    blob.upload_from_string(contenido, content_type="application/pdf")
    url = blob.generate_signed_url(expiration=timedelta(hours=2))  # URL válida por 2 horas
    return {"gcs_path": url, "blob_name": blob.name}

def generar_url_firmada(document_id: str, expiracion_horas: int = 1) -> str:
    client = storage.Client()
    bucket = client.bucket(os.getenv("GCS_BUCKET_NAME"))
    blob = bucket.blob(f"documentos/{document_id}.pdf")

    url = blob.generate_signed_url(
        expiration=timedelta(hours=expiracion_horas),
        method="GET"
    )
    return url

