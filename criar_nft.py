import json
import hashlib
import requests
import sys
from ecdsa import SigningKey, SECP256k1

API_URL = "http://localhost:8082/enviar_transacao"

def gerar_hash_unico(nome, descricao, url_midia):
    texto = nome + descricao + url_midia
    return hashlib.sha256(texto.encode('utf-8')).hexdigest()

def assinar_transacao(transacao, chave_privada_hex):
    chave = SigningKey.from_string(bytes.fromhex(chave_privada_hex), curve=SECP256k1)
    mensagem = json.dumps(transacao, sort_keys=True).encode()
    assinatura = chave.sign(mensagem).hex()
    return assinatura

def criar_transacao_nft(endereco, chave_privada, nome, descricao, url_midia, royalties_percentual):
    hash_unico = gerar_hash_unico(nome, descricao, url_midia)
    transacao = {
        "tipo": "nft",
        "de": endereco,
        "dados": {
            "nome": nome,
            "descricao": descricao,
            "url_midia": url_midia,
            "unicidade": hash_unico,
            "royalties": {
                "criador": endereco,
                "percentual": royalties_percentual
            }
        }
    }
    assinatura = assinar_transacao(transacao, chave_privada)
    transacao["assinatura"] = assinatura
    return transacao

def enviar_transacao(transacao):
    try:
        resposta = requests.post(API_URL, json=transacao)
        resposta.raise_for_status()
    except Exception as e:
        print(f"Erro ao enviar transação: {e}")
        sys.exit(1)
    return resposta

def main():
    print("=== Criar NFT na Tibúrcio Blockchain ===")
    endereco = input("Digite seu endereço público: ").strip()
    chave_privada = input("Digite sua chave privada (hex): ").strip()
    nome = input("Nome do NFT: ").strip()
    descricao = input("Descrição do NFT: ").strip()
    url_midia = input("URL do vídeo/imagem do NFT: ").strip()
    royalties_str = input("Percentual de royalties (ex: 10): ").strip()
    try:
        royalties_percentual = int(royalties_str)
        if royalties_percentual < 0 or royalties_percentual > 100:
            raise ValueError
    except:
        print("Percentual inválido. Usando padrão 10%.")
        royalties_percentual = 10

    transacao = criar_transacao_nft(endereco, chave_privada, nome, descricao, url_midia, royalties_percentual)
    print("\nTransação NFT criada:")
    print(json.dumps(transacao, indent=2))

    confirmar = input("Enviar esta transação para a blockchain? (s/n): ").strip().lower()
    if confirmar != 's':
        print("Operação cancelada.")
        sys.exit(0)

    resposta = enviar_transacao(transacao)
    print(f"Resposta do servidor: {resposta.status_code} - {resposta.text}")
    if resposta.status_code == 200:
        print("NFT criado e registrado com sucesso!")
    else:
        print("Falha ao registrar NFT.")

if __name__ == "__main__":
    main()
