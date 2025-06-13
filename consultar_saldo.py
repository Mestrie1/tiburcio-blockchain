import json

def carregar_blockchain():
    try:
        with open("blockchain.txt", "r") as f:
            blockchain = json.load(f)
        return blockchain
    except:
        return []

def calcular_saldo(endereco):
    blockchain = carregar_blockchain()
    saldo = 0
    for bloco in blockchain:
        transacoes = bloco.get("transacoes", [])
        for tx in transacoes:
            if tx["destino"] == endereco:
                saldo += tx["quantidade"]
            if tx["origem"] == endereco:
                saldo -= tx["quantidade"]
        # Recompensa de mineração (se existir)
        if bloco.get("minerador") == endereco:
            saldo += bloco.get("recompensa", 0)
    return saldo

if __name__ == "__main__":
    endereco = input("Digite o endereço da carteira para ver saldo: ")
    saldo = calcular_saldo(endereco)
    print(f"Saldo da carteira {endereco}: {saldo} $Tib")
