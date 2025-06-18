import ecdsa
import hashlib
import json
import requests

# Dados da transação
remetente = "wjkg42GwXUNsspnPNJ7L8qZJo3sBt8NWWrKG7TAKwpJF8KYaM"
destinatario = "6cfbbc026bcc5af04604dae3197e11b9ccc1a907"
quantidade = 10  # Pode alterar para a quantidade que quiser

# Sua chave privada hex (guarde em segredo)
chave_privada_hex = "3686e0565bb9aa36846cd956022c1fdbb7ec26f4f92213ac1ea8155551c40584"

def assinar_transacao(remetente, destinatario, quantidade, chave_privada_hex):
    tx = {
        "remetente": remetente,
        "destinatario": destinatario,
        "quantidade": quantidade
    }
    # Serializa transação ordenando chaves para assinatura consistente
    tx_json = json.dumps(tx, sort_keys=True).encode()
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(chave_privada_hex), curve=ecdsa.SECP256k1)
    assinatura = sk.sign(tx_json).hex()
    return assinatura, tx

assinatura, tx = assinar_transacao(remetente, destinatario, quantidade, chave_privada_hex)

# Transação completa com assinatura
transacao_assinada = {
    "remetente": remetente,
    "destinatario": destinatario,
    "quantidade": quantidade,
    "assinatura": assinatura
}

print("Transação assinada pronta para enviar:")
print(json.dumps(transacao_assinada, indent=2))

# Envia para seu servidor local (ajuste IP e porta se precisar)
url = "http://127.0.0.1:8081/nova_transacao"
response = requests.post(url, json=transacao_assinada)

print("Resposta do servidor:")
print(response.status_code, response.text)

