import requests
import hashlib
import base64
from ecdsa import SigningKey, SECP256k1

# Sua chave privada em hex (guarde em segurança!)
chave_privada_hex = "406eff534d4366cb4a14301252f7a26db7cb29587457afb6ad42a3a25c637d74"

# Cria a chave de assinatura
sk = SigningKey.from_string(bytes.fromhex(chave_privada_hex), curve=SECP256k1)

remetente = "497f981404fb415023347cb62589652fa1d52f62eb00bcba07b3383b6721b294"
destinatario = input("Endereço destinatário (para): ").strip()
quantidade = int(input("Quantidade a transferir: "))

# Cria a mensagem a ser assinada
mensagem = f"remetente:{remetente};destinatario:{destinatario};quantidade:{quantidade}"
hash_mensagem = hashlib.sha256(mensagem.encode()).digest()

# Gera a assinatura
assinatura = sk.sign(hash_mensagem)
assinatura_b64 = base64.b64encode(assinatura).decode()

# Cria a transação com assinatura e chave pública (para validação)
transacao = {
    "de": remetente,
    "para": destinatario,
    "quantidade": quantidade,
    "assinatura": assinatura_b64,
    "chave_publica": sk.get_verifying_key().to_string().hex()
}

# Envia para o servidor
url = "http://127.0.0.1:8082/nova_transacao"
response = requests.post(url, json=transacao)

print(response.json())
