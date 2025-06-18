import json

BLOCKCHAIN_FILE = "blockchain.json"

def consultar_saldo(endereco):
    saldo = 0
    try:
        with open(BLOCKCHAIN_FILE, "r") as f:
            blockchain = json.load(f)
            for bloco in blockchain:
                for tx in bloco["transacoes"]:
                    if tx["de"] == endereco:
                        saldo -= tx["quantidade"]
                    if tx["para"] == endereco:
                        saldo += tx["quantidade"]
    except:
        pass
    return saldo

if __name__ == "__main__":
    endereco = input("Digite o endereço da carteira: ").strip()
    saldo = consultar_saldo(endereco)
    print(f"💰 Saldo de {endereco}: {saldo} $Tiburcio")
