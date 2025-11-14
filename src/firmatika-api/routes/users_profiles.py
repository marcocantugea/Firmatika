import uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, Body, File,HTTPException,Request, UploadFile
from services.blockchain import wallet_existe_en_red
from services.users import get_user_by_id,update_user, update_user_password

router = APIRouter()

@router.post("/users/{user_id}/wallet")
def link_user_wallet(user_id: str, payload: dict = Body(...)):
    wallet_address = payload.get("wallet_address")
    if not wallet_address:
        raise HTTPException(status_code=400, detail="Direccion de Wallet es requerida")

    try:
        if not wallet_existe_en_red(wallet_address):
            raise HTTPException(status_code=400, detail="Direccion de Wallet no existe en la red blockchain")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error verificando wallet en blockchain: {str(e)}")

    user= get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user.wallet = wallet_address

    update_user(user)

    return {"message": f"Wallet {wallet_address} linked to user {user_id}"}

@router.put("/users/{user_id}/password")
def change_user_password(user_id: str, payload: dict = Body(...)):
    new_password = payload.get("new_password")
    if not new_password:
        raise HTTPException(status_code=400, detail="Nueva contraseña es requerida")

    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    update_user_password(user_id, new_password)

    return {"message": "Contraseña actualizada correctamente"}