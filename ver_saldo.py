import json
import os

SALDO_FILE = "saldos.json"

def carregar_saldos():
    if os.path.exists(SALDO_FILE):
        with open(SALDO_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

endereco = input("Digite o endereço da carteira para ver saldo: ")
saldos = carregar_saldos()
saldo = saldos.get(endereco, 0)
print(f"💰 Saldo da carteira {endereco}: {saldo} Tibúrcio")
