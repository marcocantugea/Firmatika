import hashlib
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from models.documentoFirmado import DocumentoFirmado
from services.documents import get_firmantes_by_document_uuid


def generar_certificado(documento: DocumentoFirmado ):

    firmantes = get_firmantes_by_document_uuid(documento.uuid)

    firmantes_nombres = ", ".join([f"{f['nombres']} {f['apellidos']}" for f in firmantes])

    # Contenido que quieres certificar
    contenido = b"hash|" + documento.hash_documento.encode() + b"; |Firmantes|" + firmantes_nombres.encode()

    # 1. Generar hash SHA-256
    hash_documento = hashlib.sha256(contenido).digest()

    # 2. Cargar la llave privada desde un archivo PEM
    with open("keys/firmatika.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,  # si tu llave está protegida con passphrase, ponla aquí
        )

    # 3. Firmar el hash con la llave privada
    signature = private_key.sign(
        hash_documento,
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    # 4. Codificar la firma en Base64
    certificate = base64.b64encode(signature).decode("utf-8")

    return certificate