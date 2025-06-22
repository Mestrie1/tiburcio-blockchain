# Tibúrcio Blockchain

Tibúrcio Blockchain é uma blockchain própria, minerável, descentralizada e fácil de usar. Permite criar carteiras, minerar blocos, transferir tokens com assinatura digital e consultar saldo via API REST. Também possui comunicação P2P para sincronização entre nós.

---

## Funcionalidades principais

- ✅ Criar carteira com chave pública e privada
- ✅ Minerar blocos (Proof of Work) e receber recompensas
- ✅ Transferir tokens online com assinatura digital
- ✅ Consultar saldo de qualquer carteira via API REST
- ✅ Comunicação P2P entre nós para manter blockchain sincronizada
- ✅ Backups automáticos dos blocos minerados

---

## Instalação e execução (Passo a passo)

1️⃣ **Instalar Termux (Android):**  
Disponível na Play Store ou site oficial.

2️⃣ **Atualizar pacotes do sistema:**  
```bash
pkg update && pkg upgrade -y


pkg install python git -y

pip install flask ecdsa


git clone https://github.com/Mestrie1/tiburcio-blockchain.git
cd tiburcio-blockchain

chmod +x start.sh
./start.sh

==== Tiburcio Blockchain ====
1) Criar carteira
2) Minerar
3) Transferir tokens
4) Sair

curl http://localhost:8082/saldo/<endereco_publico>

python3 p2p_node.py

Suporte
📲 Telegram oficial: Grupo Tibúrcio Blockchain
https://t.me/+jU0ocN7fQx5mYTBh

