import os
import time
import shutil
from datetime import datetime

CAMINHO_BLOCKCHAIN = "blockchain.json"
PASTA_BACKUPS = "backups"
INTERVALO_SEGUNDOS = 300  # 5 minutos (ajuste se quiser)

def criar_backup():
    if not os.path.exists(CAMINHO_BLOCKCHAIN):
        print(f"Arquivo {CAMINHO_BLOCKCHAIN} não encontrado. Nada a salvar.")
        return
    if not os.path.exists(PASTA_BACKUPS):
        os.makedirs(PASTA_BACKUPS)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo_backup = os.path.join(PASTA_BACKUPS, f"blockchain_backup_{timestamp}.json")

    shutil.copy2(CAMINHO_BLOCKCHAIN, arquivo_backup)
    print(f"Backup criado: {arquivo_backup}")

def main():
    print("Backup automático da blockchain iniciado.")
    while True:
        criar_backup()
        time.sleep(INTERVALO_SEGUNDOS)

if __name__ == "__main__":
    main()
