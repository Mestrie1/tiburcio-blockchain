import ecdsa
import hashlib
import base64

def assinar_transacao(mensagem, chave_privada_hex):
    chave_privada_bytes = bytes.fromhex(chave_privada_hex)
    sk = ecdsa.SigningKey.from_string(chave_privada_bytes, curve=ecdsa.SECP256k1)
    assinatura = sk.sign(mensagem.encode())
    return base64.b64encode(assinatura).decode()

if __name__ == "__main__":
    # 📬 Dados da transação:
    remetente = "wjkg42GwXUNsspnPNJ7L8qZJo3sBt8NWWrKG7TAKwpJF8KYaM"
    destinatario = "2ZaDcYVC9YmPZzLMLqiL4BxiesGBKuPdn1Go5oM16N2RE8N6X9"
    quantidade = 50

    mensagem = f"remetente:{remetente};destinatario:{destinatario};quantidade:{quantidade}"

    chave_privada = "3686e0565bb9aa36846cd956022c1fdbb7ec26f4f92213ac1ea8155551c40584"

    assinatura = assinar_transacao(mensagem, chave_privada)

    print("\n📜 Mensagem para assinatura:")
    print(mensagem)
    print("\n✅ Assinatura gerada:")
    print(assinatura)
