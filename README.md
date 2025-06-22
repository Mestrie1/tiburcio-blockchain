Tiburcio Blockchain
Tibúrcio Blockchain é uma blockchain própria, minerável, descentralizada e fácil de usar, que permite criar carteiras, minerar blocos, transferir tokens online com assinatura digital e consultar saldo via API REST. O sistema inclui comunicação P2P entre nós e salva toda a blockchain no servidor para garantir segurança e continuidade.

Para começar, clone o repositório com o comando git clone (https://github.com/Mestrie1/tiburcio-blockchain.git) Depois entre na pasta do projeto e dê permissão ao script de inicialização com (chmod +x start.sh). Para rodar o projeto, use (./start.sh) que abre um menu interativo com opções para criar carteira, minerar, transferir tokens, iniciar servidores e sair.

Com o servidor rodando, consulte o saldo de qualquer carteira pelo terminal usando curl http://localhost:8082/saldo/<endereco_publico>, substituindo <endereco_publico> pelo endereço que deseja consultar.

As funções principais do projeto estão divididas em arquivos: app.py (API REST), minerador.py (minerador PoW), p2p_server.py (servidor P2P), send_tx.py (envio e assinatura de transações) e start.sh (script para facilitar a execução).

(telegram https://t.me/+jU0ocN7fQx5mYTBh)
