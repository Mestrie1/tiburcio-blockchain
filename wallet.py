from ecdsa import SigningKey, SECP256k1
import hashlib
import binascii

def gerar_chaves():
    # Gera chave privada (SigningKey) usando curva SECP256k1 (como Bitcoin)
    chave_privada = SigningKey.generate(curve=SECP256k1)
    chave_publica = chave_privada.get_verifying_key()
    
    # Codifica para hex para salvar/exibir
    chave_priv_hex = chave_privada.to_string().hex()
    chave_pub_hex = chave_publica.to_string().hex()
    
    return chave_priv_hex, chave_pub_hex

def assinar_mensagem(chave_priv_hex, mensagem):
    chave_priv = SigningKey.from_string(bytes.fromhex(chave_priv_hex), curve=SECP256k1)
    assinatura = chave_priv.sign(mensagem.encode())
    return assinatura.hex()

def verificar_assinatura(chave_pub_hex, mensagem, assinatura_hex):
    chave_pub = SigningKey.from_string(bytes.fromhex(chave_pub_hex), curve=SECP256k1).get_verifying_key()
    assinatura = bytes.fromhex(assinatura_hex)
    try:
        return chave_pub.verify(assinatura, mensagem.encode())
    except:
        return False

if __name__ == "__main__":
    priv, pub = gerar_chaves()
    print("Chave Privada:", priv)
    print("Chave Pública:", pub)

    msg = "Enviar 10 tokens para endereço XYZ"
    assinatura = assinar_mensagem(priv, msg)
    print("Assinatura:", assinatura)

    valida = verificar_assinatura(pub, msg, assinatura)
    print("Assinatura válida?", valida)

