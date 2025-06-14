from ecdsa import SigningKey, VerifyingKey, SECP256k1

def gerar_chaves():
    chave_privada = SigningKey.generate(curve=SECP256k1)
    chave_publica = chave_privada.get_verifying_key()
    return chave_privada, chave_publica

def assinar_mensagem(chave_privada, mensagem):
    return chave_privada.sign(mensagem.encode('utf-8'))

def verificar_assinatura(chave_publica, mensagem, assinatura):
    try:
        return chave_publica.verify(assinatura, mensagem.encode('utf-8'))
    except:
        return False
