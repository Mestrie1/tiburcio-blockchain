import json
import os

ARQUIVO_BLOCKCHAIN = "blockchain.json"

def carregar_blockchain():
    if os.path.exists(ARQUIVO_BLOCKCHAIN):
        with open(ARQUIVO_BLOCKCHAIN, "r") as f:
            return json.load(f)
    return []

def calcular_saldo(endereco):
    blockchain = carregar_blockchain()
    saldo = 0
    for bloco in blockchain:
        for transacao in bloco["transacoes"]:
            if transacao["para"] == endereco:
                saldo += transacao["quantidade"]
            if transacao["de"] == endereco:
                saldo -= transacao["quantidade"]
    return saldo

if __name__ == "__main__":
    endereco = input("Digite o endereço da carteira para ver saldo: ")
    saldo = calcular_saldo(endereco)
    print(f"💰 Saldo da carteira {endereco}: {saldo} TiBúrcio")
