import hashlib
import base64
from ecdsa import SigningKey, SECP256k1

# Sua chave privada (hexadecimal)
CHAVE_PRIVADA_HEX = "c5d921995fbce18c18b3e63d3a44472d4c8601214fc8fe886a86e148b3664aad"

def gerar_assinatura(mensagem, chave_privada_hex):
    chave_privada_bytes = bytes.fromhex(chave_privada_hex)
    sk = SigningKey.from_string(chave_privada_bytes, curve=SECP256k1)
    hash_mensagem = hashlib.sha256(mensagem.encode()).digest()
    assinatura = sk.sign(hash_mensagem)
    return base64.b64encode(assinatura).decode()

if __name__ == "__main__":
    remetente = input("Endereço remetente (público): ").strip()
    destinatario = input("Endereço destinatário: ").strip()
    quantidade = float(input("Quantidade a enviar: "))

    mensagem = f"remetente:{remetente};destinatario:{destinatario};quantidade:{quantidade}"
    print("\n📜 Mensagem para assinatura:")
    print(mensagem)

    assinatura = gerar_assinatura(mensagem, CHAVE_PRIVADA_HEX)

    print("\n✅ Assinatura gerada (base64):")
    print(assinatura)
