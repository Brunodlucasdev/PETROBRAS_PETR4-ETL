# Databricks notebook source
path_bronze = "abfss://bronze@datalakebrunodev.dfs.core.windows.net/*.csv"

df_bronze = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(path_bronze)
)
display(df_bronze)

# COMMAND ----------

df_bronze = df_bronze.filter(df_bronze["Open"] != "PETR4.SA")

# COMMAND ----------

from pyspark.sql.functions import col, round, to_date

# 1. Renomeia as colunas e remove o Adj Close
df_silver = (
    df_bronze
    .withColumnRenamed("Date", "Data")
    .withColumnRenamed("Open", "Abertura")
    .withColumnRenamed("High", "Maxima")
    .withColumnRenamed("Low", "Minima")
    .withColumnRenamed("Close", "Fechamento")
    .drop("Adj Close")
)

# 2. Formata a data e arredonda os valores para 2 casas decimais
df_silver = (
    df_silver
    .withColumn("Data", to_date(col("Data")))
    .withColumn("Abertura", round(col("Abertura"), 2))
    .withColumn("Maxima", round(col("Maxima"), 2))
    .withColumn("Minima", round(col("Minima"), 2))
    .withColumn("Fechamento", round(col("Fechamento"), 2))
)

# 3. Métrica de variação diária e remoção de nulos
df_silver = df_silver.withColumn("Variacao", round(col("Fechamento") - col("Abertura"), 2)).dropna()

display(df_silver)

# COMMAND ----------

# Definindo o caminho para a camada Silver
STORAGE_ACCOUNT = "datalakebrunodev"
CONTAINER_SILVER = "silver"
path_silver = f"abfss://{CONTAINER_SILVER}@{STORAGE_ACCOUNT}.dfs.core.windows.net/dados_acoes_delta"

print("Salvando os dados limpos na Camada Silver no formato Delta...")

# Salvando o DataFrame em formato Delta, sobrescrevendo se já existir
(
    df_silver.write
    .format("delta")
    .mode("overwrite")
    .save(path_silver)
)

print(f"Sucesso! Dados salvos na camada Silver no caminho:\n{path_silver}")