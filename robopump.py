import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

PUBLIC_KEY = os.getenv("SOLANA_PUBLIC")
PRIVATE_KEY = os.getenv("SOLANA_PRIVATE")

VALOR_ENTRADA = 0.0005  # 0.50 SOL em valor
LUCRO_MINIMO = 1.0       # 100% (dobrar)
INTERVALO_CHECAGEM = 10  # segundos

def fetch_tokens():
    try:
        r = requests.get("https://pump.fun/api/markets/live")
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print("Erro ao buscar tokens:", e)
    return []

def calcula_score(token):
    volume = float(token.get("volumeUsd24h", 0))
    variacao = float(token.get("priceChangePercent", 0))
    holders = int(token.get("holderCount", 0))
    score = (volume / 10000) * 40 + variacao * 2 + holders * 0.5
    return score

def comprar_token(token):
    print(f"🔥 COMPRANDO {token['name']} com {VALOR_ENTRADA} SOL")
    print(f"📈 Volume: {token.get('volumeUsd24h')} | Holders: {token.get('holderCount')} | % Pump: {token.get('priceChangePercent')}")
    # Aqui você implementaria chamada real para comprar usando SDK (Jupiter ou Pump.fun API)
    # Exemplo: client.send_transaction(...)
    # 🚧 Esta parte depende da integração futura com transações reais Solana

def monitorar_venda(token):
    print(f"⏳ Monitorando {token['name']} para venda com lucro de +{int(LUCRO_MINIMO*100)}%...")
    # Aqui você integraria com API de preço e executaria venda quando atingir lucro

def main():
    print("🤖 Robô sniper Pump.fun (modo real/simulado) iniciado.")
    while True:
        tokens = fetch_tokens()
        for token in tokens:
            score = calcula_score(token)
            variacao = float(token.get("priceChangePercent", 0))
            if score > 85 and variacao > 5:
                comprar_token(token)
                monitorar_venda(token)
        time.sleep(INTERVALO_CHECAGEM)

if __name__ == "__main__":
    main()

