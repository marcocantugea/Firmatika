import os
import json
from dotenv import load_dotenv
from web3 import Web3
from models.documentoFirmado import BlockchainTx
load_dotenv()

def firmar_hash_en_blockchain(hash_documento: str) -> dict:
    w3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_RPC_URL")))
    private_key = os.getenv("BLOCKCHAIN_PRIVATE_KEY")
    contract_address = Web3.to_checksum_address(os.getenv("BLOCKCHAIN_CONTRACT_ADDRESS"))

    # Cargar ABI
    with open("../firmatika-blockchain/artifacts/contracts/FimaDigital.sol/FirmaDigital.json") as f:
        abi = json.load(f)["abi"]

    contrato = w3.eth.contract(address=contract_address, abi=abi)
    cuenta = w3.eth.account.from_key(private_key)
    print(cuenta.address)

    contrato.functions.firmarDocumento(hash_documento).call()

    nonce = w3.eth.get_transaction_count(cuenta.address,"pending")
    gas_price = w3.eth.gas_price

    gas_estimate = contrato.functions.firmarDocumento(hash_documento).estimate_gas({"from": cuenta.address})
    gas_price = w3.eth.gas_price
    costo_total = gas_estimate * gas_price
    print(w3.from_wei(costo_total, "ether"))



    tx = contrato.functions.firmarDocumento(hash_documento).build_transaction({
        "from": cuenta.address,
        "nonce": nonce,
        "gas": 200000,
        "gasPrice": gas_price
    })

    print(tx)

    firmado = cuenta.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(firmado.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
    print("Transaction hash:", tx_hash.hex())
    print("Transaction receipt:")
    print(receipt)

    result= BlockchainTx(
        tx_hash=tx_hash.hex(),
        block_number=receipt.blockNumber,
        timestamp=w3.eth.get_block(receipt.blockNumber).timestamp,
        network=os.getenv("NET_SELECTED")
    )

    return result.dict()

from web3 import Web3

def wallet_existe_en_red(address: str) -> bool:
    w3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_RPC_URL")))
    if not Web3.is_address(address):
        return False  # Formato inválido

    balance = w3.eth.get_balance(address)
    tx_count = w3.eth.get_transaction_count(address)

    return balance > 0 or tx_count > 0