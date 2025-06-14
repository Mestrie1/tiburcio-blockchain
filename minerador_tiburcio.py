import json
import time
import hashlib

ARQUIVO_BLOCKCHAIN = 'blockchain.json'
ENDERECO_DESTINO = "wjkg42GwXUNsspnPNJ7L8qZJo3sBt8NWWrKG7TAKwpJF8KYaM"
RECOMPENSA = 50
MAX_SUPPLY = 21000000  # Limite total de moedas, igual Bitcoin (21 milhões)

def carregar_blockchain():
    try:
        with open(ARQUIVO_BLOCKCHAIN, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"blocos": []}

def salvar_blockchain(blockchain):
    with open(ARQUIVO_BLOCKCHAIN, 'w') as f:
        json.dump(blockchain, f, indent=4)

def calcular_hash_bloco(bloco):
    bloco_serializado = json.dumps(bloco, sort_keys=True).encode()
    return hashlib.sha256(bloco_serializado).hexdigest()

def calcular_total_moedas(blockchain):
    total = 0
    for bloco in blockchain['blocos']:
        for transacao in bloco.get('transacoes', []):
            if transacao['origem'] == 'recompensa':
                total += transacao['quantidade']
    return total

def minerar_novo_bloco(blockchain, transacoes):
    indice = len(blockchain['blocos'])
    timestamp = time.time()
    anterior = blockchain['blocos'][-1]['hash'] if blockchain['blocos'] else "0" * 64

    bloco = {
        "indice": indice,
        "timestamp": timestamp,
        "transacoes": transacoes,
        "anterior": anterior,
    }
    bloco['hash'] = calcular_hash_bloco(bloco)

    blockchain['blocos'].append(bloco)
    salvar_blockchain(blockchain)
    print(f"Bloco {indice} minerado e salvo!")

def main():
    blockchain = carregar_blockchain()
    
    while True:
        total_moedas = calcular_total_moedas(blockchain)
        if total_moedas >= MAX_SUPPLY:
            print(f"Limite máximo de {MAX_SUPPLY} TiBúrcio atingido. Mineração encerrada.")
            break
        
        transacoes = [{"origem": "recompensa", "destino": ENDERECO_DESTINO, "quantidade": RECOMPENSA}]
        minerar_novo_bloco(blockchain, transacoes)
        time.sleep(2)

if __name__ == "__main__":
    main()
