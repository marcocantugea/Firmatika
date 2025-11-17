import os
import json
from dotenv import load_dotenv
from web3 import Web3
from models.documentoFirmado import BlockchainTx
from fastapi import HTTPException

load_dotenv()


def firmar_hash_en_blockchain(hash_documento: str,nombre_completo: str, nombre_documento: str, descripcion_documento: str, delegada: bool,user_wallet: str=None) -> dict:
    try:
        w3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_RPC_URL")))
        private_key = os.getenv("BLOCKCHAIN_PRIVATE_KEY")
        contract_address = Web3.to_checksum_address(os.getenv("BLOCKCHAIN_CONTRACT_ADDRESS"))

        with open("../firmatika-blockchain/artifacts/contracts/FimaDigital.sol/FirmaDigital.json") as f:
            abi = json.load(f)["abi"]

        contrato = w3.eth.contract(address=contract_address, abi=abi)
        cuenta = w3.eth.account.from_key(private_key)

        nonce = w3.eth.get_transaction_count(cuenta.address, "pending")
        gas_price = w3.eth.gas_price

        # firmantes = contrato.functions.obtenerFirmantes(hash_documento).call()
        # ya_firmo = any(f[0].lower() == cuenta.address.lower() for f in firmantes)

        # if ya_firmo:
        #     raise ValueError("Esta wallet ya firmó este documento")

        gas_estimate = 0
        if(delegada and user_wallet):
            gas_estimate = contrato.functions.firmarDelegada(hash_documento,nombre_completo, nombre_documento, descripcion_documento, user_wallet).estimate_gas({"from": cuenta.address})
        else:
            gas_estimate =contrato.functions.firmarDocumento(hash_documento, nombre_completo, nombre_documento, descripcion_documento, delegada).estimate_gas({"from": cuenta.address})
        
        costo_total = gas_estimate * gas_price

        print("Costo estimado:", w3.from_wei(costo_total, "ether"))

        tx = None
        if(delegada and user_wallet):
            tx = contrato.functions.firmarDelegada(hash_documento, nombre_completo, nombre_documento, descripcion_documento, user_wallet).build_transaction({
                "from": cuenta.address,
                "nonce": nonce,
                "gas": gas_estimate,
                "gasPrice": gas_price
            })
        else:
            tx = contrato.functions.firmarDocumento(hash_documento, nombre_completo, nombre_documento, descripcion_documento, delegada).build_transaction({
                "from": cuenta.address,
                "nonce": nonce,
                "gas": gas_estimate,
                "gasPrice": gas_price
        })

        if tx is None:
            raise ValueError("Error al construir la transacción")

        firmado = cuenta.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(firmado.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)

        result = BlockchainTx(
            tx_hash=tx_hash.hex(),
            block_number=receipt.blockNumber,
            timestamp=w3.eth.get_block(receipt.blockNumber).timestamp,
            network=os.getenv("NET_SELECTED")
        )

        return result.dict()
    except Exception as e:
        print("Error al firmar en blockchain:", str(e))
        raise HTTPException(status_code=400, detail=str(e))


def wallet_existe_en_red(address: str) -> bool:
    w3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_RPC_URL")))
    if not Web3.is_address(address):
        return False  # Formato inválido

    balance = w3.eth.get_balance(address)
    tx_count = w3.eth.get_transaction_count(address)

    return balance > 0 or tx_count > 0