import requests

API_URL = "http://localhost:8082"  # ou a porta que seu app.py está rodando

def listar_nfts(endereco):
    url = f"{API_URL}/nfts/{endereco}"
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        nfts = resposta.json()
        if nfts:
            for nft in nfts:
                print(f"ID: {nft['id']} - Nome: {nft['nome']} - URL: {nft['url_midia']}")
        else:
            print("Nenhum NFT encontrado para essa carteira.")
    except Exception as e:
        print("Erro ao consultar NFTs:", e)

if __name__ == "__main__":
    endereco = input("Digite seu endereço público: ")
    listar_nfts(endereco)
