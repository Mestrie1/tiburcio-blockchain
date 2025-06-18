import hashlib
import os

def gerar_chave_privada():
    return os.urandom(32).hex()

def gerar_endereco_publico(chave_privada):
    return hashlib.sha256(chave_privada.encode()).hexdigest()

if __name__ == "__main__":
    chave_privada = gerar_chave_privada()
    endereco_publico = gerar_endereco_publico(chave_privada)

    print("Sua chave privada (guarde com segurança!):")
    print(chave_privada)
    print()
    print("📬 Seu endereço público:")
    print(endereco_publico)

