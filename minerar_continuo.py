import json
import hashlib
import time
import os

CAMINHO_BLOCKCHAIN = 'blockchain.json'
RECOMPENSA_MINERACAO = 50
ENDERECO_MINERADOR = 'wjkg42GwXUNsspnPNJ7L8qZJo3sBt8NWWrKG7TAKwpJF8KYaM'

def carregar_blockchain():
    if not os.path.exists(CAMINHO_BLOCKCHAIN):
        return []
    with open(CAMINHO_BLOCKCHAIN, 'r') as f:
        return json.load(f)

def salvar_blockchain(blockchain):
    with open(CAMINHO_BLOCKCHAIN, 'w') as f:
        json.dump(blockchain, f, indent=4)

def calcular_hash_bloco(bloco):
    bloco_serializado = json.dumps(bloco, sort_keys=True).encode()
    return hashlib.sha256(bloco_serializado).hexdigest()

def criar_bloco(novo_index, anterior_hash):
    timestamp = time.time()
    transacoes = []
    recompensa = {
        'para': ENDERECO_MINERADOR,
        'quantidade': RECOMPENSA_MINERACAO
    }
    bloco = {
        'index': novo_index,
        'timestamp': timestamp,
        'transacoes': transacoes,
        'recompensa': recompensa,
        'anterior': anterior_hash
    }
    bloco['hash'] = calcular_hash_bloco(bloco)
    return bloco

def minerar_continuamente():
    blockchain = carregar_blockchain()
    if blockchain:
        ultimo_bloco = blockchain[-1]
        novo_index = ultimo_bloco['index'] + 1
        anterior_hash = ultimo_bloco['hash']
    else:
        novo_index = 0
        anterior_hash = '0'

    while True:
        novo_bloco = criar_bloco(novo_index, anterior_hash)
        blockchain.append(novo_bloco)
        salvar_blockchain(blockchain)
        print(f'✅ Novo bloco #{novo_index} minerado com recompensa de {RECOMPENSA_MINERACAO} TiBúrcio!')
        novo_index += 1
        anterior_hash = novo_bloco['hash']
        time.sleep(1)  # Tempo entre blocos (1 segundo). Pode ajustar aqui.

if __name__ == '__main__':
    minerar_continuamente()
