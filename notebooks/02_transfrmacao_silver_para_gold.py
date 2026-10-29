# Databricks notebook source
# 1. Lê os dados salvos na camada Silver
STORAGE_ACCOUNT = "datalakebrunodev"
path_silver = f"abfss://silver@{STORAGE_ACCOUNT}.dfs.core.windows.net/dados_acoes_delta"

# Carregando a tabela delta
df_silver = spark.read.format("delta").load(path_silver)

# COMMAND ----------

print("Iniciando a transformação para a Camada Gold usando SQL...")

# 1. Cria uma visão temporária em memória para consulta SQL
df_silver.createOrReplaceTempView("tabela_silver")

# 2. Executa a agregação mensal via SQL
df_gold = spark.sql("""
    SELECT 
        YEAR(Data) AS Ano,
        MONTH(Data) AS Mes,
        ROUND(AVG(Fechamento), 2) AS Media_Fechamento,
        ROUND(MAX(Maxima), 2) AS Maxima_Mensal,
        ROUND(AVG(Variacao), 2) AS Media_Variacao_Diaria
    FROM tabela_silver
    GROUP BY YEAR(Data), MONTH(Data)
    ORDER BY Ano, Mes
""")

# Exibe o resultado das métricas calculadas
display(df_gold)

# 3. Salva a tabela agregada na camada Gold do Data Lake
STORAGE_ACCOUNT = "datalakebrunodev"
path_gold = f"abfss://gold@{STORAGE_ACCOUNT}.dfs.core.windows.net/metricas_financeiras_mensais"

(
    df_gold.write
    .format("delta")
    .mode("overwrite")
    .save(path_gold)
)

print(f"Sucesso! Tabela Gold criada no caminho:\n{path_gold}")