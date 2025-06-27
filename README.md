# 🧙‍♂️ Tibúrcio Blockchain

Um projeto de blockchain espiritual e descentralizado, inspirado no combate à escuridão e na disseminação de luz, com validação por Prova de Trabalho (PoW) e transações assinadas com criptografia ECDSA.

## ✨ Destaques

* 🔐 **Transações assinadas** com ECDSA (curva SECP256k1)
* ⚒️ **Minerador PoW** com recompensas para minerador configurável
* 🌐 **Full node** e **sincronização P2P** automática
* 📡 **Serviço de saldo** via API (Flask)
* 📬 **Envio de transações online** com assinatura
* 🛠️ **Menu interativo** via script `start.sh` para fácil uso
* 🙏 Carregando energia positiva na blockchain para espalhar luz pelo mundo

---

## 📦 Requisitos

* Python 3.8+
* Bibliotecas Python:

  * `flask`
  * `ecdsa`
  * `requests`

Instale com:

```bash
pip install flask ecdsa requests
```

Ou use:

```bash
pip install -r requirements.txt
```

---

## ⚡ Como iniciar (guia para iniciantes)

### 1. Clonar o repositório

```bash
git clone https://github.com/Mestrie1/tiburcio-blockchain.git
cd tiburcio-blockchain
chmod +x start.sh
```

### 2. Configurar Git (se for seu primeiro commit)

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seuemail@exemplo.com"
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Usar o script de inicialização

O projeto possui um menu interativo que facilita a execução de todos os serviços. Basta rodar:

```bash
./start.sh
```

Você verá o menu:

```
=== Tiburcio Blockchain - Menu ===
1) Iniciar todos os servidores (Full Node + P2P + Saldo + API)
2) Minerar (minerador.py)
3) Enviar transação
4) Consultar saldo
5) Consolidar blocos (recuperar saldo)
0) Sair
```

* **1)** Inicia todos os serviços em segundo plano:

  * Full Node (armazena blockchain)
  * P2P Server (porta 5001)
  * Saldo Server (porta 5003)
  * API Server (porta 8082)

* **2)** Inicia o minerador solicitando sua carteira pública

* **3)** Envia transações assinadas online de forma automática

* **4)** Consulta saldo de qualquer endereço via API

* **5)** Consolida blocos em arquivo único para recuperar saldo

* **0)** Sai do menu

---

## 🔧 Usando o menu

1. Após rodar `./start.sh`, digite o número da opção e pressione Enter.
2. Siga as instruções na tela para cada opção.
3. Para voltar ao menu principal, aguarde a conclusão da ação.
4. Para sair a qualquer momento, pressione `Ctrl+C` ou escolha a opção 0.

---

## 📖 Estrutura de pastas

```text
tiburcio-blockchain/
├── app.py             # API Flask para receber transações e consultar saldo
├── minerador.py       # Bot de mineração PoW automátic
├── p2p_server.py      # Servidor P2P para sincronização de blocos
├── saldo_server.py    # Servidor HTTP para consulta de saldo
├── tiburcio_full_node.py  # Implementação do full node
├── send_tx.py         # Envio de transações assinadas via HTTP
├── start.sh           # Script de inicialização com menu interativo
├── consolidar_blockchain.py  # Consolida backups em blockchain.json
├── backups/           # Backups de blocos gerados automaticamente
├── README.md          # Este arquivo de documentação
└── requirements.txt   # Lista de dependências Python
```

---

## 🙏 Missão e visão

O Tibúrcio Blockchain foi criado para **espalhar luz e positividade**, combatendo as trevas com cada bloco minerado. Nossa comunidade busca unir tecnologia, espiritualidade e descentralização para fazer do mundo um lugar melhor.

Contribua, compartilhe e ajude a crescer essa rede de luz!

---

## 🤝 Contribuições

1. Faça um fork do projeto
2. Crie sua branch: `git checkout -b minha-contribuicao`
3. Faça suas alterações e commit: `git commit -m "Minha contribuição"`
4. Envie para o GitHub: `git push origin minha-contribuicao`
5. Abra um Pull Request

---

## 📜 Licença

Este projeto é open source, use, estude e compartilhe!
