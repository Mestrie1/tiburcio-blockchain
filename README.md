Tibúrcio Blockchain
Tibúrcio Blockchain é uma blockchain própria, minerável, descentralizada e fácil de usar. Permite criar carteiras, minerar blocos, transferir tokens com assinatura digital e consultar saldo via API REST. Também possui comunicação P2P para sincronização entre nós.

Funcionalidades principais
Criar carteira com chave pública e privada

Minerar blocos (Proof of Work) e receber recompensas

Transferir tokens online com assinatura digital

Consultar saldo de qualquer carteira via API REST

Sincronização P2P entre nós para manter blockchain atualizada

Requisitos
Termux (em Android) ou Linux/macOS com terminal

Python 3 instalado

Conexão com internet para instalar dependências

Passo a passo para instalar e rodar
Instalar Termux (se estiver no Android):
Baixe na Google Play ou site oficial.

Abrir Termux e atualizar os pacotes:

bash
Copiar código
pkg update && pkg upgrade -y
Instalar Python e Git:

bash
Copiar código
pkg install python git -y
Instalar bibliotecas Python necessárias:

bash
Copiar código
pip install flask ecdsa
Clonar repositório Tibúrcio Blockchain:

bash
Copiar código
git clone https://github.com/Mestrie1/tiburcio-blockchain.git
cd tiburcio-blockchain
Dar permissão para o script de inicialização:

bash
Copiar código
chmod +x start.sh
Rodar o script de inicialização:

bash
Copiar código
./start.sh
No menu, criar carteira (opção 1) e anotar seu endereço público e chave privada.

Para minerar (opção 2), informe seu endereço público para receber as recompensas.

Para transferir tokens (opção 3), informe os dados solicitados.

Consultar saldo via API REST
Com o servidor rodando, no Termux ou terminal separado, use:

bash
Copiar código
curl http://localhost:8082/saldo/<seu_endereco_publico>
Substitua <seu_endereco_publico> pelo endereço gerado na carteira.

Backup automático
O sistema salva a blockchain no arquivo blockchain.json e faz backup automático em arquivos com timestamp para evitar perda de dados.

Contato
Telegram para dúvidas e suporte: https://t.me/+jU0ocN7fQx5mYTBh

Assim qualquer pessoa, mesmo sem experiência, consegue instalar, rodar e interagir com a blockchain Tibúrcio.

Quer que eu te envie agora um script bash que automatiza todo esse processo do setup até rodar o start.sh?







Você disse:
Quero esse redme quero fazer ELE NO TMEUX PARA SUBIR PARA GITHUB


O ChatGPT disse:
Perfeito! Vou te enviar agora o README.md completo que você pode copiar e colar diretamente no Termux. Ele já está pronto para ser salvo e enviado para o seu repositório no GitHub.

Aqui está o conteúdo do README.md:

markdown
Copiar código
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
3️⃣ Instalar Python e Git:

bash
Copiar código
pkg install python git -y
4️⃣ Instalar bibliotecas necessárias:

bash
Copiar código
pip install flask ecdsa
5️⃣ Clonar o repositório oficial:

bash
Copiar código
git clone https://github.com/Mestrie1/tiburcio-blockchain.git
cd tiburcio-blockchain
6️⃣ Dar permissão e iniciar o script:

bash
Copiar código
chmod +x start.sh
./start.sh
Menu interativo
diff
Copiar código
==== Tiburcio Blockchain ====
1) Criar carteira
2) Minerar
3) Transferir tokens
4) Sair
Criar carteira (1): Gera endereço público e chave privada.

Minerar (2): Inicia mineração e gera tokens de recompensa.

Transferir (3): Realiza transações entre carteiras.

Consultar saldo via API REST
Com o servidor app.py rodando:

bash
Copiar código
curl http://localhost:8082/saldo/<endereco_publico>
Substitua <endereco_publico> pelo seu endereço gerado.

Comunicação entre nós (P2P)
Para rodar o nó P2P e sincronizar com outros:

bash
Copiar código
python3 p2p_node.py
Digite o endereço do nó que deseja sincronizar, exemplo:

cpp
Copiar código
http://192.168.1.10:5000
Backup automático
A blockchain é salva no arquivo blockchain.json.
Backups automáticos são gerados com timestamps, por exemplo:

pgsql
Copiar código
blockchain_backup_20250622.json
Você pode copiar backups para outro local:

bash
Copiar código
cp blockchain_backup_*.json /sdcard/Download/
Suporte
📲 Telegram oficial: Grupo Tibúrcio Blockchain

Vamos espalhar a luz! ✨

yaml
Copiar código

---

