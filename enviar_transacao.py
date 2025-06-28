#!/usr/bin/env python3
import requests
import hashlib
import base64
import os
from ecdsa import SigningKey, SECP256k1

# Configuração da chave privada do remetente (hex)
chave_privada_hex = "406eff534d4366cb4a14301252f7a26db7cb29587457afb6ad42a3a25c637d74"

# Cria a chave de assinatura ECDSA
sk = SigningKey.from_string(bytes.fromhex(chave_privada_hex), curve=SECP256k1)

def assinar_transacao(remetente, destinatario, quantidade):
    mensagem = f"remetente:{remetente};destinatario:{destinatario};quantidade:{quantidade}"
    hash_mensagem = hashlib.sha256(mensagem.encode()).digest()
    assinatura = sk.sign(hash_mensagem)
    return base64.b64encode(assinatura).decode()

def obter_chave_publica():
    vk = sk.get_verifying_key()
    return vk.to_string().hex()

def main():
    remetente = input("Endereço público (de): ").strip()
    destinatario = input("Endereço do destinatário (para): ").strip()
    quantidade = int(input("Quantidade a transferir: ").strip())

    assinatura_b64 = assinar_transacao(remetente, destinatario, quantidade)
    chave_pub_hex = obter_chave_publica()

    payload = {
        "de": remetente,
        "para": destinatario,
        "quantidade": quantidade,
        "assinatura": assinatura_b64,
        "chave_publica": chave_pub_hex
    }

    url = "http://127.0.0.1:8082/enviar_transacao"
    try:
        resp = requests.post(url, json=payload)
        print(f"Status Code: {resp.status_code}")
        try:
            print("Resposta JSON:", resp.json())
        except ValueError:
            print("Conteúdo da resposta:", resp.text)
    except requests.exceptions.ConnectionError as e:
        print("Erro de conexão ao enviar transação:", e)

if __name__ == "__main__":
    main()
