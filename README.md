# 📈 Pipeline ETL de Dados Financeiros (PETR4) — Azure & Databricks

Este projeto é um pipeline de Engenharia de Dados ponta a ponta (End-to-End) para extração, armazenamento, transformação e análise de cotações históricas da ação **PETR4.SA** (Petrobras), utilizando a **Arquitetura Medalhão** na nuvem Azure com **Databricks** e **PySpark**.

---

## 🏗️ Arquitetura da Solução

```text
[ Yahoo Finance API ]
        │
        ▼ (Python & yfinance)
[ Extração Local / WSL ]
        │
        ▼ (Azure Blob SDK)
[ Azure Data Lake Gen2 ] ──► Camada Bronze: RAW (.csv)
        │
        ▼ (PySpark & Unity Catalog)
[ Azure Databricks Serverless ]
        │
        ▼ (Delta Lake)
[ Azure Data Lake Gen2 ] ──► Camada Silver: Delta Format (dados tratados)
```

---

## 🚀 Tecnologias Utilizadas

- **Linguagens:** Python 3.x, SQL, PySpark, Bash Shell
- **Provedor de Nuvem:** Azure (Azure Data Lake Storage Gen2, Access Connectors)
- **Processamento Distribuído:** Azure Databricks (Serverless & Unity Catalog)
- **Armazenamento:** Delta Lake
- **Desenvolvimento Local:** WSL (Windows Subsystem for Linux), Git/GitHub, `python-dotenv`

---

## 📂 Estrutura do Repositório

```text
.
├── data/                    # Diretório local para dados temporários (raw)
├── notebooks/               # Notebooks PySpark desenvolvidos no Databricks
│   └── 01_transformacao_bronze_para_silver.py
├── scripts/                 # Scripts de automação e extração local
│   ├── extract_data.py      # Extração da API yfinance + upload para Azure Bronze
│   └── run_pipeline.sh      # Bash script para execução automatizada
├── .gitignore               # Proteção de arquivos sensíveis (.env, venv, data)
├── requirements.txt         # Dependências do projeto Python
└── README.md                # Documentação do projeto
```

---

## 🔄 Fluxo de Dados (Medallion Architecture)

### 1. Camada Bronze (Raw)

- Extração automatizada via script Python consumindo a biblioteca `yfinance`.
- Limpeza de dados inválidos no cabeçalho.
- Envio direto para o container `bronze` no **Azure Data Lake Storage Gen2** em formato `.csv`.

### 2. Camada Silver (Cleansing & Standardization)

- Processamento distribuído no **Azure Databricks** utilizando PySpark e o protocolo **ABFSS**.
- Tratamento de tipagem de dados, padronização dos nomes das colunas para português, arredondamento monetário e cálculo da métrica de variação diária (`Fechamento - Abertura`).
- Salvamento performático no container `silver` no formato open-source **Delta Lake**.

---

## 🔒 Segurança e Boas Práticas

- **Credenciais protegidas:** nenhuma chave de acesso é commitada no código. Uso de variáveis de ambiente com `.env` e `.gitignore`.
- **Governança com Unity Catalog:** integração segura entre Databricks Serverless e Azure ADLS Gen2 através de *Storage Credentials*, *Access Connectors* e *External Locations*.

---

## 🛠️ Como Executar Localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/Brunodlucasdev/Projeto-de-ETL-.git
cd Projeto-de-ETL-
```

### 2. Configurar o ambiente virtual Python

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com a string de conexão da sua conta Azure:

```env
AZURE_STORAGE_CONNECTION_STRING="sua_connection_string_aqui"
```

### 4. Executar a extração

```bash
chmod +x scripts/run_pipeline.sh
./scripts/run_pipeline.sh
```

---

## 🗺️ Próximos Passos

- [ ] Camada Gold (agregações e métricas analíticas)
- [ ] Orquestração do pipeline (Databricks Workflows)
- [ ] Dashboard de visualização dos dados
