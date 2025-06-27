import json
import os

# Lista todos os arquivos de backup no diretório atual
arquivos_backup = sorted([f for f in os.listdir() if f.startswith("backup_") and f.endswith(".json")])
blockchain_consolidada = []

for nome_arquivo in arquivos_backup:
    with open(nome_arquivo, "r") as f:
        try:
            blocos = json.load(f)
            if isinstance(blocos, list):
                blockchain_consolidada.extend(blocos)
            else:
                print(f"{nome_arquivo} ignorado (não é uma lista)")
        except Exception as e:
            print(f"Erro ao ler {nome_arquivo}: {e}")

# Remove blocos duplicados (por hash)
hashes_vistos = set()
blockchain_final = []
for bloco in blockchain_consolidada:
    hash_bloco = bloco.get("hash")
    if hash_bloco and hash_bloco not in hashes_vistos:
        blockchain_final.append(bloco)
        hashes_vistos.add(hash_bloco)

# Salva no arquivo final
with open("blockchain.json", "w") as f:
    json.dump(blockchain_final, f, indent=4)

print(f"Consolidação concluída com {len(blockchain_final)} blocos salvos em blockchain.json")
