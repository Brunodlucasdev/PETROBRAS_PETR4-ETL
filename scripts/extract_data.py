import yfinance as yf
import pandas as pd
import os
from datetime import datetime

# Configurações do ativo (Petrobras como exemplo)
TICKER = "PETR4.SA" 
START_DATE = "2023-01-01"
# Pega a data de hoje automaticamente
END_DATE = datetime.today().strftime('%Y-%m-%d')

# Caminho onde o arquivo será salvo
OUTPUT_DIR = "../data/raw"
OUTPUT_FILE = f"{OUTPUT_DIR}/dados_acoes.csv"

def extrair_dados():
    print(f"Iniciando extração de dados para {TICKER}...")
    print(f"Período: {START_DATE} até {END_DATE}")
    
    # 1. Baixando os dados usando yfinance
    df = yf.download(TICKER, start=START_DATE, end=END_DATE)
    
    # 2. O yfinance coloca a 'Date' (Data) como índice. Vamos transformar em coluna normal.
    df.reset_index(inplace=True)
    
    # 3. Criando o diretório caso ele não exista
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 4. Salvando os dados no formato CSV
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Sucesso! Arquivo CSV salvo em: {OUTPUT_FILE}")
    print(f"Foram extraídas {len(df)} linhas de dados.")

if __name__ == "__main__":
    extrair_dados()