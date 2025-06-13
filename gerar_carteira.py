import os
import hashlib
import base58

def gerar_chave_privada():
    return os.urandom(32).hex()

def gerar_endereco(chave_privada):
    chave_bytes = bytes.fromhex(chave_privada)
    hash_publico = hashlib.sha256(chave_bytes).digest()
    endereco = base58.b58encode_check(hash_publico).decode()
    return endereco

chave_privada = gerar_chave_privada()
endereco = gerar_endereco(chave_privada)

print("🔑 Sua chave privada (guarde com segurança!):")
print(chave_privada)
print("\n📬 Seu endereço público:")
print(endereco)
