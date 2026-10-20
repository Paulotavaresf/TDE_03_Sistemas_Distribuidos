# Sistema de Deteção de Fraude com Apache Kafka

Este projeto simula um sistema de deteção de fraude em tempo real utilizando **Apache Kafka**, Python e um banco de dados para persistência.

## 🏗️ Arquitetura do Sistema

1. **Produtor (Producer):** 
   - Gera transações bancárias simuladas e aleatórias a cada 3 segundos.
   - Envia as mensagens para um tópico do Kafka.
   - Segue estritamente a estrutura de dados JSON definida (ID da transação, ID do cliente, valor, país, cidade e hora).

2. **Consumidor (Consumer):**
   - Lê as transações do tópico do Kafka em tempo real.
   - Guarda **todas** as transações recebidas no banco de dados.
   - Aplica regras de negócio para identificar potenciais fraudes e exibe alertas no terminal.

## 🚨 Regras de Deteção de Fraude

* **ALTO_VALOR:** Transações com valor superior ou igual a 10.000.
* **TEMPO_60s:** O mesmo cliente realiza 4 transações num intervalo inferior a 60 segundos.
* **GEO_10m:** O mesmo cliente realiza transações em cidades diferentes (`city`) num período de até 10 minutos.

---

## 🛠️ Como Executar o Projeto

### Pré-requisitos
* Docker e Docker Compose instalados.
* Python 3.8+ instalado.

### 1. Iniciar o Kafka
Na pasta raiz do projeto, suba o container do Kafka utilizando o Docker Compose:
```bash
docker-compose up -d