import yfinance as yf
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

# Carrega a chave de forma segura
load_dotenv()
AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "bronze"
cd
TICKER = "PETR4.SA" 
START_DATE = "2023-01-01"
END_DATE = datetime.today().strftime('%Y-%m-%d')
OUTPUT_DIR = "../data/raw"
OUTPUT_FILE = f"{OUTPUT_DIR}/dados_acoes.csv"
BLOB_NAME = f"dados_acoes_{END_DATE}.csv"

def extrair_e_enviar_dados():
    print(f"Extraindo dados de {TICKER}...")
    df = yf.download(TICKER, start=START_DATE, end=END_DATE)
    df.reset_index(inplace=True)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    
    print("Iniciando upload para o Azure Data Lake (Camada Bronze)...")
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)
    
    with open(OUTPUT_FILE, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
        
    print(f"Sucesso! Arquivo '{BLOB_NAME}' salvo no contêiner '{CONTAINER_NAME}'.")

if __name__ == "__main__":
    extrair_e_enviar_dados()