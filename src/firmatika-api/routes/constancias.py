import uuid
import hashlib
import qrcode
import os
from reportlab.lib.utils import ImageReader
from textwrap import wrap
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime, timedelta
from fastapi import APIRouter,HTTPException,Response
from services.constancia import exist_constancia_documento
from services.blockchain import get_url_transaction_blockchain
from dotenv import load_dotenv


router = APIRouter()
load_dotenv()

@router.post("/constancia/{document_uuid}/crear")
async def crear_constancia(document_uuid: str):
    from services.constancia import create_constancia_documento
    try:
        if exist_constancia_documento(document_uuid):
            raise HTTPException(status_code=400, detail="La constancia para este documento ya existe")
        
        constancia_documento = create_constancia_documento(document_uuid)
        return constancia_documento
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/constancia/{constancia_uuid}")
async def obtener_constancia(constancia_uuid: str):
    from services.constancia import get_constancia_documento_by_uuid
    try:
        constancia_documento = get_constancia_documento_by_uuid(constancia_uuid)
        return constancia_documento
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.get("/constancia/{constancia_uuid}/download")
async def descargar_constancia(constancia_uuid: str):
    from services.constancia import get_constancia_documento_by_uuid
    try:
        constancia_documento = get_constancia_documento_by_uuid(constancia_uuid)
       # Crear PDF en memoria
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        x=20
        # Encabezado
        c.setFont("Helvetica-Bold", 16)
        c.drawString(x, 750, "Constancia de Documento Digital Firmado")

        # Datos del documento
        c.setFont("Helvetica", 12)
        c.drawString(x, 720, f"Documento: {constancia_documento.documento.nombre}")
        c.drawString(x, 700, f"Nombre Archivo: {constancia_documento.documento.gcs_path['blob_name']}")
        c.drawString(x, 680, f"Hash: {constancia_documento.hash}")
        c.drawString(x, 660, f"Descripción: {constancia_documento.documento.descripcion}")
        url= get_url_transaction_blockchain(constancia_documento.documento.blockchain_tx.tx_hash)
        url_documento = "transacción en blockchain: " + url if constancia_documento.documento.blockchain_tx else "N/A"
        lineas = wrap(url_documento, width=90)
        y = 640
        for linea in lineas:
            c.drawString(x, y, linea)
            text_width = c.stringWidth(linea, "Helvetica", 12)
            c.linkURL(url, (x, y, x + text_width, y + 12), relative=0)
            y -= 20  # espacio entre líneas

        c.setFont("Helvetica-Bold", 16)
        c.drawString(x, y-20, "Firmas")
        c.setFont("Helvetica", 12)
        #c.drawString(x, 660, f"transacción en blockchain: " + )
        y -= 40
        # Firmantes
        for firma in constancia_documento.firmas:
            LabelDelegate = "Sí" if firma.firma_delegada else "No"
            c.drawString(x, y, f"Firmante: {firma.nombres}  {firma.apellidos}")
            c.drawString(x, y-15, f"Email: {firma.email}")
            c.drawString(x, y-35, f"Delegada: {LabelDelegate} - Fecha: {firma.fecha_firma.isoformat() if firma.fecha_firma else 'N/A'}")
            c.drawString(x, y-45, "----------------------------------------")

            lineas= wrap("transacción en blockchain: " + get_url_transaction_blockchain(firma.tx_hash.tx_hash) if firma.tx_hash else "N/A", width=90)
            for linea in lineas:
                c.drawString(x, y-60, linea)
                y -= 15 

            y -= 80  # espacio entre firmantes

        lines = wrap(f"Certificado de la Constancia: {constancia_documento.constancia.certificado_constancia}", width=80)
        for line in lines:
            c.drawString(x, y, line)
            y -= 15
    
        # Generea QR
        url_constancia = os.getenv("HOST_FRONT_URL") + f"/constancia/verificar?qr={constancia_uuid}"
        qr = qrcode.QRCode(box_size=4, border=2)
        qr.add_data(url_constancia)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buffer_img = BytesIO()
        img.save(buffer_img, format="PNG")
        buffer_img.seek(0)
        qr_image = ImageReader(buffer_img)

        # 3. Dibujar el QR al final del PDF
        # (asumiendo que ya tienes tu canvas `c`)
        c.drawString(100, 100, "Ver constancia en línea:")
        c.drawImage(qr_image, 250, 60, width=100, height=100)  # ajusta posición y tamaño
        buffer_img.close()

        # Finalizar PDF
        c.showPage()
        c.save()

        buffer.seek(0)
        pdf_bytes = buffer.getvalue()
        buffer.close()

        # Retornar como archivo descargable
        return Response(content=pdf_bytes,
                        media_type="application/pdf",
                        headers={"Content-Disposition": f"attachment; filename=constancia_{constancia_uuid}.pdf"})

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))