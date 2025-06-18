import hashlib
import json
import requests
import time

NODE_URL = 'http://127.0.0.1:8081'
CARTEIRA_MINERADOR = 'wjkg42GwXUNsspnPNJ7L8qZJo3sBt8NWWrKG7TAKwpJF8KYaM'
RECOMPENSA_MINERACAO = 50  # Valor da recompensa por bloco minerado

def hash_bloco(bloco):
    bloco_string = json.dumps(bloco, sort_keys=True).encode()
    return hashlib.sha256(bloco_string).hexdigest()

def minerar_bloco(transacoes, dificuldade=4):
    nonce = 0
    prefixo_alvo = '0' * dificuldade
    while True:
        bloco = {
            'nonce': nonce,
            'transacoes': transacoes,
            'timestamp': time.time()
        }
        hash_do_bloco = hash_bloco(bloco)
        if hash_do_bloco.startswith(prefixo_alvo):
            bloco['hash'] = hash_do_bloco
            return bloco
        nonce += 1

def minerador():
    print("⚙️ Mineração iniciada...")
    response = requests.get(f"{NODE_URL}/pendentes")
    transacoes = response.json()

    # ⏺️ Adiciona transação de recompensa para o minerador
    transacoes.append({
        'remetente': 'RECOMPENSA',
        'destinatario': CARTEIRA_MINERADOR,
        'quantidade': RECOMPENSA_MINERACAO,
        'assinatura': ''
    })

    bloco = minerar_bloco(transacoes)
    resposta = requests.post(f"{NODE_URL}/receber_bloco", json=bloco)
    if resposta.status_code == 201:
        print(f"✅ Bloco minerado e enviado com sucesso! +{RECOMPENSA_MINERACAO} Tibúrcio ganhos.")
    else:
        print(f"Erro ao enviar bloco: {resposta.status_code} {resposta.text}")

if __name__ == '__main__':
    minerador()
