# Tibúrcio Blockchain

Projeto de blockchain próprio, minerável e descentralizado, com funcionalidades completas: criação de carteira, mineração, transferências online e consulta de saldo, inspirado no Bitcoin mas com características próprias.

---

## Índice

- [Descrição](#descrição)  
- [Pré-requisitos](#pré-requisitos)  
- [Instalação](#instalação)  
- [Como rodar](#como-rodar)  
- [Menu Interativo](#menu-interativo)  
- [Endpoints da API](#endpoints-da-api)  
- [Comandos disponíveis](#comandos-disponíveis)  
- [Contribuição](#contribuição)  
- [Licença](#licença)  

---

## Descrição

Este projeto implementa uma blockchain chamada Tibúrcio, com sistema próprio de mineração Proof of Work, transações assinadas, rede P2P e armazenamento dos blocos no servidor. Possui interface via terminal e servidor Flask para consultas e transações online.

---

## Pré-requisitos

- Python 3.8 ou superior  
- Pip  
- Git  
- Bibliotecas Python necessárias: Flask, requests, ecdsa

---

## Instalação

```bash
# Clonar o repositório
git clone https://github.com/Mestrie1/tiburcio-blockchain.git
cd tiburcio-blockchain

# Instalar dependências
pip install -r requirements.txt
