import time
import hashlib
import json

# Endereço do minerador (exemplo)
ENDERECO_MINERADOR = "wjkg42GwXUNsspnPNJ7L8qZJo3sBt8NWWrKG7TAKwpJF8KYaM"

# Configurações iniciais
dificuldade = 5
ajuste_cada_blocos = 100
blocos_minerados_desde_ultimo_ajuste = 0
ultimo_ajuste = time.time()

# Função para calcular o hash do bloco
def calcular_hash(bloco):
    bloco_string = json.dumps(bloco, sort_keys=True).encode()
    return hashlib.sha256(bloco_string).hexdigest()

# Função que simula a mineração do bloco
def minerar_bloco(numero_bloco, dificuldade):
    prefixo_zeros = "0" * dificuldade
    nonce = 0
    while True:
        bloco = {
            "numero": numero_bloco,
            "nonce": nonce,
            "minerador": ENDERECO_MINERADOR,
            "timestamp": time.time()
        }
        hash_bloco = calcular_hash(bloco)
        if hash_bloco.startswith(prefixo_zeros):
            return bloco, hash_bloco
        nonce += 1

# Função para ajustar a dificuldade
def ajustar_dificuldade():
    global dificuldade, ultimo_ajuste, blocos_minerados_desde_ultimo_ajuste

    agora = time.time()
    tempo_decorrido = agora - ultimo_ajuste
    tempo_ideal = ajuste_cada_blocos * 10  # 10 segundos por bloco (ajuste se quiser)

    if tempo_decorrido < tempo_ideal * 0.9:
        dificuldade += 1
        print(f"🔺 Dificuldade aumentada para {dificuldade}")
    elif tempo_decorrido > tempo_ideal * 1.1 and dificuldade > 1:
        dificuldade -= 1
        print(f"🔻 Dificuldade reduzida para {dificuldade}")

    ultimo_ajuste = agora
    blocos_minerados_desde_ultimo_ajuste = 0

# Função principal de mineração
def main():
    global blocos_minerados_desde_ultimo_ajuste

    numero_bloco = 2275  # Pode carregar do blockchain atual para continuar
    print("Minerador Tibúrcio iniciado!")

    while True:
        print(f"Minerando bloco {numero_bloco} com dificuldade {dificuldade}...")
        bloco, hash_bloco = minerar_bloco(numero_bloco, dificuldade)
        print(f"Bloco {numero_bloco} minerado! Hash: {hash_bloco}")

        # Atualize seu blockchain.json aqui com o novo bloco
        # (implemente a lógica para salvar o bloco na cadeia)

        # Atualiza saldo do minerador (simulado)
        saldo = 113650 + numero_bloco  # Só exemplo, ajuste seu saldo real
        print(f"Saldo atual do minerador ({ENDERECO_MINERADOR}): {saldo} TiBúrcio\n")

        numero_bloco += 1
        blocos_minerados_desde_ultimo_ajuste += 1

        if blocos_minerados_desde_ultimo_ajuste >= ajuste_cada_blocos:
            ajustar_dificuldade()

if __name__ == "__main__":
    main()
