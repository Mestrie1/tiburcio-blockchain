import os
import json

BACKUP_DIR = "backups"
OUTPUT_FILE = "blockchain.json"

def carregar_blocos_backup(caminho_arquivo):
    try:
        with open(caminho_arquivo, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Erro ao ler {caminho_arquivo}: {e}")
        return []

def consolidar_blockchain():
    blocos = []
    blocos_ids = set()

    # Lista todos os arquivos .json na pasta de backups, ordenados pelo nome
    arquivos = sorted([f for f in os.listdir(BACKUP_DIR) if f.endswith(".json")])

    print(f"🔎 Encontrados {len(arquivos)} arquivos de backup para consolidar...")

    for arquivo in arquivos:
        caminho = os.path.join(BACKUP_DIR, arquivo)
        blocos_do_backup = carregar_blocos_backup(caminho)
        for bloco in blocos_do_backup:
            indice = bloco.get("indice")
            hash_bloco = bloco.get("hash")
            identificador = (indice, hash_bloco)
            # Adiciona apenas se ainda não estiver presente
            if identificador not in blocos_ids:
                blocos.append(bloco)
                blocos_ids.add(identificador)

    # Ordena todos os blocos pelo índice
    blocos = sorted(blocos, key=lambda b: b.get("indice", 0))

    # Salva o blockchain consolidado
    with open(OUTPUT_FILE, "w") as f:
        json.dump(blocos, f, indent=4)

    print(f"✅ Blockchain consolidado salvo em: {OUTPUT_FILE}")
    print(f"📦 Total de blocos: {len(blocos)}")

if __name__ == "__main__":
    consolidar_blockchain()
