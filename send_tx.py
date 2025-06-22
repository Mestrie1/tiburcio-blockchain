import socket
import json
import time
import hashlib
import base64
from ecdsa import SigningKey, SECP256k1

def gerar_chave_publica_hex(chave_privada_hex):
    sk = SigningKey.from_string(bytes.fromhex(chave_privada_hex), curve=SECP256k1)
    vk = sk.get_verifying_key()
    return vk.to_string("compressed").hex()  # chave pública compressa em hex

def gerar_assinatura(chave_privada_hex, mensagem):
    chave_privada_bytes = bytes.fromhex(chave_privada_hex)
    sk = SigningKey.from_string(chave_privada_bytes, curve=SECP256k1)
    hash_msg = hashlib.sha256(mensagem.encode()).digest()
    assinatura = sk.sign(hash_msg)
    return base64.b64encode(assinatura).decode()

def send_transaction(tx, ip='127.0.0.1', port=5001):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        s.send(json.dumps(tx).encode())
        s.close()
        print("Transação enviada:", tx)
    except Exception as e:
        print("Erro ao enviar transação:", e)

if __name__ == "__main__":
    print("=== Enviar transação assinada ===")
    sender = input("Endereço público (de): ").strip()
    chave_privada = input("Chave privada (hex): ").strip()
    recipient = input("Endereço do destinatário (para): ").strip()
    amount_str = input("Quantidade a transferir: ").strip()

    try:
        amount = float(amount_str)
    except ValueError:
        print("Quantidade inválida! Use um número.")
        exit(1)

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

    send_transaction(tx)
