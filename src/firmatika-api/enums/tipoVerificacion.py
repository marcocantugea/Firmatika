from enum import Enum

class TipoVerificacion(str, Enum):
    WALLET = "wallet"
    DELEGADA = "delegada"
    BIOMETRIA = "biometría"