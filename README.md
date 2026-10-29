# 📈 Pipeline ETL de Dados Financeiros (PETR4) — Azure & Databricks

Pipeline de Engenharia de Dados **End-to-End** que coleta, armazena, transforma e agrega cotações históricas da ação **PETR4.SA** (Petrobras), seguindo a **Arquitetura Medalhão** (Bronze → Silver → Gold) na nuvem Azure com **Databricks**, **PySpark** e **Delta Lake**.

---

## 🏗️ Arquitetura da Solução

```text
[ Yahoo Finance API ]
        │
        ▼  Python + yfinance + azure-storage-blob
[ Extração Local (WSL) ]
        │
        ▼
[ Azure Data Lake Gen2 ] ──► 🥉 Bronze: dados brutos (.csv)
        │
        ▼  PySpark + Unity Catalog (ABFSS)
[ Azure Databricks Serverless ]
        │
        ▼
[ Azure Data Lake Gen2 ] ──► 🥈 Silver: dados limpos e padronizados (Delta)
        │
        ▼  Spark SQL (Temporary View + agregações)
[ Azure Data Lake Gen2 ] ──► 🥇 Gold: métricas mensais para análise (Delta)
```

---

## 🚀 Tecnologias Utilizadas

- **Linguagens:** Python 3.x, SQL, PySpark, Bash Shell
- **Nuvem:** Azure Data Lake Storage Gen2 (com *Hierarchical Namespace*), Access Connectors
- **Processamento distribuído:** Azure Databricks (Serverless & Unity Catalog)
- **Formato de armazenamento:** Delta Lake
- **Bibliotecas Python:** `yfinance`, `azure-storage-blob`, `python-dotenv`
- **Desenvolvimento local:** WSL (Windows Subsystem for Linux), Git/GitHub

---

## 📂 Estrutura do Repositório

```text
.
├── data/                                      # Diretório local para dados temporários (raw)
├── notebooks/                                 # Notebooks desenvolvidos no Databricks
│   ├── 01_Transformacao_bronze_para_silver.py # PySpark: limpeza e padronização
│   └── 02_agregacao_silver_para_gold.py       # Spark SQL: agregações mensais
├── scripts/                                   # Automação e extração local
│   ├── extract_data.py                        # Extração da API yfinance + upload para a Bronze
│   └── run_pipeline.sh                        # Execução automatizada da extração
├── .gitignore                                 # Proteção de arquivos sensíveis (.env, venv, data)
├── requirements.txt                           # Dependências Python
└── README.md                                  # Documentação do projeto
```

---

## 🔄 Fluxo de Dados (Medallion Architecture)

### 1. Extração e ingestão (ambiente local)

- **Coleta via API:** script Python com `yfinance` extrai as cotações históricas (Abertura, Fechamento, Máxima, Mínima e Volume) em formato CSV.
- **Credenciais protegidas:** a string de conexão da Azure é carregada por `python-dotenv` a partir de um arquivo `.env`, que fica fora do repositório pelo `.gitignore`.
- **Upload automatizado:** com `azure-storage-blob`, o script envia o CSV direto para o container `bronze`.

### 🥉 Camada Bronze (Dados Brutos)

- Os dados chegam exatamente como foram extraídos, em formato **CSV**.
- O Databricks lê o container pelo protocolo seguro **ABFSS** e carrega os dados em um Spark DataFrame.
- Nesta etapa são removidos artefatos da API, como o texto do *ticker* gravado por engano no cabeçalho.

### 🥈 Camada Silver (Limpeza e Padronização)

Transformações feitas com **PySpark**:

- **Padronização:** colunas renomeadas para português (`Open` → `Abertura`, `High` → `Maxima` etc.) e remoção de colunas não utilizadas, como `Adj Close`.
- **Tipagem e formatação:** coluna de data convertida para o tipo `Date` e valores monetários arredondados para 2 casas decimais.
- **Métrica calculada:** coluna `Variacao` = `Fechamento - Abertura`.
- **Qualidade:** remoção de valores nulos com `.dropna()`.
- **Armazenamento:** gravação no container `silver` em **Delta Lake** (transações ACID, *Time Travel* e alta performance de leitura).

### 🥇 Camada Gold (Regras de Negócio e Agregação)

Camada pronta para consumo por analistas de BI e cientistas de dados:

- **Modelagem com Spark SQL:** a tabela Silver é carregada como uma *Temporary View*.
- **Agregações por Ano e Mês:**
  - Média de fechamento mensal
  - Pico máximo do mês
  - Média da variação diária
- **Armazenamento:** dataset sumarizado gravado no container `gold` em formato **Delta**, concluindo o ciclo do pipeline.

---

## 🔒 Segurança e Governança

- **Sem credenciais no código:** nenhuma chave ou connection string é commitada. O acesso local usa variáveis de ambiente (`.env`) protegidas pelo `.gitignore`.
- **Unity Catalog:** o acesso do Databricks ao Data Lake é feito por *Storage Credentials*, *Access Connectors* e *External Locations*, sem expor chaves de acesso nos notebooks.
- **Custo otimizado:** conta de armazenamento com redundância local (LRS) e processamento em Databricks Serverless.

---

## 🛠️ Como Executar a Extração Localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/Brunodlucasdev/Projeto-de-ETL-.git
cd Projeto-de-ETL-
```

### 2. Criar o ambiente virtual e instalar as dependências

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
AZURE_STORAGE_CONNECTION_STRING="sua_connection_string_aqui"
```

### 4. Executar a extração

```bash
chmod +x scripts/run_pipeline.sh
./scripts/run_pipeline.sh
```

### 5. Rodar as transformações no Databricks

Importe os notebooks da pasta `notebooks/` no seu workspace e execute em ordem:

1. `01_Transformacao_bronze_para_silver.py`
2. `02_agregacao_silver_para_gold.py`

> **Pré-requisito:** Unity Catalog configurado com *Storage Credential* e *External Locations* apontando para os containers `bronze`, `silver` e `gold`.

---

## 🎯 Competências Demonstradas

Engenharia de Dados · ETL/ELT · Arquitetura Medalhão · Azure Data Lake Gen2 · Databricks · PySpark · Spark SQL · Delta Lake · Unity Catalog · Python · Bash · Git/GitHub · Segurança de credenciais

---

## 👤 Autor

**Bruno** — [GitHub](https://github.com/Brunodlucasdev)
