import dotenv
import os
from google.cloud import storage

dotenv.load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GCS_CREDENTIALS_PATH")

def subir_pdf_a_gcs(document_id: str, contenido: bytes) -> str:
    client = storage.Client()
    bucket = client.bucket(os.getenv("GCS_BUCKET_NAME"))
    blob = bucket.blob(f"documentos/{document_id}.pdf")
    blob.upload_from_string(contenido, content_type="application/pdf")
    return blob.name
