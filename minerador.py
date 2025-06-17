import requests
import hashlib
import json
import time

URL_SERVIDOR = 'https://tiburcio-blockchain-10.onrender.com'  # URL do seu projeto no Render

def calcular_hash(bloco):
    bloco_codificado = json.dumps(bloco, sort_keys=True).encode()
    return hashlib.sha256(bloco_codificado).hexdigest()

def minerar_bloco(transacoes, indice, hash_anterior, dificuldade):
    nonce = 0
    while True:
        bloco = {
            'indice': indice,
            'timestamp': time.time(),
            'transacoes': transacoes,
            'nonce': nonce,
            'hash_anterior': hash_anterior
        }
        hash_bloco = calcular_hash(bloco)
        if hash_bloco.startswith('0' * dificuldade):
            return bloco, hash_bloco
        nonce += 1

def obter_blockchain():
    try:
        resposta = requests.get(f'{URL_SERVIDOR}/blockchain')
        if resposta.status_code == 200:
            return resposta.json()
        else:
            print('❌ Erro ao obter blockchain do servidor.')
            return None
    except Exception as e:
        print(f'❌ Erro de conexão: {e}')
        return None

def enviar_bloco(bloco):
    try:
        resposta = requests.post(f'{URL_SERVIDOR}/novo_bloco', json=bloco)
        if resposta.status_code == 200:
            print('✅ Bloco adicionado à blockchain!')
        else:
            print('❌ Erro ao enviar bloco.')
    except Exception as e:
        print(f'❌ Erro de conexão ao enviar bloco: {e}')

def minerar():
    blockchain = obter_blockchain()
    if not blockchain:
        return

    ultimo_bloco = blockchain[-1]
    indice = ultimo_bloco['indice'] + 1
    hash_anterior = ultimo_bloco['hash']
    transacoes = [{"de": "minerador", "para": "Você", "quantidade": 1}]
    dificuldade = 4  # Aumente se quiser mais dificuldade

    print('⚙️  Mineração iniciada...')
    bloco, hash_bloco = minerar_bloco(transacoes, indice, hash_anterior, dificuldade)
    bloco['hash'] = hash_bloco
    enviar_bloco(bloco)

if __name__ == '__main__':
    while True:
        minerar()
