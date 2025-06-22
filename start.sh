#!/bin/bash

while true; do
  echo "==== Tiburcio Blockchain ===="
  echo "1) Criar carteira"
  echo "2) Minerar"
  echo "3) Transferir tokens"
  echo "4) Sair"
  read -p "Escolha uma opção: " opcao

  case $opcao in
    1)
      echo "Criando carteira..."
      python gerar_carteira.py
      ;;
    2)
      read -p "Digite seu endereço público para receber recompensas: " endereco
      python minerador.py << EOF
$endereco
EOF
      ;;
    3)
      read -p "Digite seu endereço público (de): " de
      read -p "Digite sua chave privada: " chave_privada
      read -p "Digite o endereço do destinatário (para): " para
      read -p "Digite a quantidade a transferir: " quantidade
      python send_tx.py --de "$de" --chave_privada "$chave_privada" --para "$para" --quantidade "$quantidade"
      ;;
    4)
      echo "Saindo..."
      break
      ;;
    *)
      echo "Opção inválida. Tente novamente."
      ;;
  esac
done

