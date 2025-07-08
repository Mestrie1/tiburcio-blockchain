import json
import requests
import hashlib
import ecdsa
import time

NFTS_FILE = "nft_loja.json"
API_URL = "http://localhost:8082/enviar_transacao"

def assinar_transacao(dados, chave_privada_hex):
    chave_privada_bytes = bytes.fromhex(chave_privada_hex)
    sk = ecdsa.SigningKey.from_string(chave_privada_bytes, curve=ecdsa.SECP256k1)
    hash_tx = hashlib.sha256(json.dumps(dados, sort_keys=True).encode()).digest()
    assinatura = sk.sign(hash_tx)
    return assinatura.hex()

def main():
    try:
        with open(NFTS_FILE, "r") as f:
            nfts = json.load(f)
    except:
        print("Erro ao carregar NFTs da loja.")
        return

    print("\nNFTs disponíveis:")
    for nft in nfts:
        print(f"[{nft['id']}] {nft['nome']} - {nft['preco']} Tibúrcio")

    id_escolhido = input("\nDigite o ID do NFT que deseja comprar: ")
    try:
        id_escolhido = int(id_escolhido)
    except:
        print("ID inválido.")
        return

    nft = next((n for n in nfts if n["id"] == id_escolhido), None)
    if not nft:
        print("NFT não encontrado.")
        return

    endereco = input("Seu endereço público: ").strip()
    chave_privada = input("Sua chave privada (hex): ").strip()

    dados_tx = {
        "tipo": "nft_compra",
        "de": endereco,
        "dados": {
            "nome": nft["nome"],
            "preco": nft["preco"],
            "imagem": nft["imagem"],
            "timestamp": time.time()
        }
    }

    assinatura = assinar_transacao(dados_tx, chave_privada)
    dados_tx["assinatura"] = assinatura

    print("\nEnviando transação para comprar o NFT...")
    resposta = requests.post(API_URL, json=dados_tx)

    print("Resposta do servidor:", resposta.status_code, "-", resposta.text)

if __name__ == "__main__":
    main()
