from ecdsa import SigningKey, SECP256k1

chave_privada_hex = input("Digite sua chave privada (hexadecimal): ").strip()

# Converter chave privada para bytes
chave_privada_bytes = bytes.fromhex(chave_privada_hex)

# Criar objeto SigningKey
sk = SigningKey.from_string(chave_privada_bytes, curve=SECP256k1)

# Obter a chave pública
vk = sk.verifying_key
chave_publica_bytes = vk.to_string()

# Formatar como hexadecimal (não comprimida)
chave_publica_hex = "04" + chave_publica_bytes.hex()

print(f"🔑 Sua chave pública (hexadecimal):\n{chave_publica_hex}")
