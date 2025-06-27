import sys
import time
import json
import hashlib
import base64
from ecdsa import SigningKey, SECP256k1

try:
    import requests
except ImportError:
    print("Erro: instale a biblioteca requests com 'pip install requests'")
    sys.exit(1)

def gerar_chave_publica_hex(chave_privada_hex):
    sk = SigningKey.from_string(bytes.fromhex(chave_privada_hex), curve=SECP256k1)
    vk = sk.get_verifying_key()
    return vk.to_string("compressed").hex()

def gerar_assinatura(chave_privada_hex, mensagem):
    sk = SigningKey.from_string(bytes.fromhex(chave_privada_hex), curve=SECP256k1)
    hash_msg = hashlib.sha256(mensagem.encode()).digest()
    assinatura = sk.sign(hash_msg)
    return base64.b64encode(assinatura).decode()

def send_transaction_http(tx, url='http://127.0.0.1:8082/enviar_transacao'):
    try:
        resp = requests.post(url, json=tx)
        print("Status Code:", resp.status_code)
        print("Resposta:", resp.text)
    except Exception as e:
        print("Erro ao enviar transação:", e)

def main():
    if len(sys.argv) != 5:
        print("Uso: python send_tx.py <endereco_de> <chave_privada_hex> <endereco_para> <quantidade>")
        return

    sender = sys.argv[1]
    chave_privada = sys.argv[2]
    recipient = sys.argv[3]
    try:
        amount = float(sys.argv[4])
    except ValueError:
        print("Quantidade inválida!")
        return

    chave_publica = gerar_chave_publica_hex(chave_privada)
    mensagem = f"remetente:{sender};destinatario:{recipient};quantidade:{amount}"
    assinatura = gerar_assinatura(chave_privada, mensagem)

    tx = {
        "de": sender,
        "para": recipient,
        "quantidade": amount,
        "assinatura": assinatura,
        "chave_publica": chave_publica,
        "timestamp": int(time.time())
    }

    send_transaction_http(tx)

if __name__ == "__main__":
    main()
