import  pandas as pd
import numpy as np

#carregando o data frame 
df_produto = pd.read_csv("/home/joaovitorandrade/Documentos/Repositórios/PTA-engenharia-de-dados/data/[Júlia] DataLake - pedidos.csv")

#lista de colunas para ajustar data/hora antes da converção 
colunas_data = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

# Converter todas as colunas para datetime
for coluna in colunas_data:
    df_produto[coluna] = pd.to_datetime(df_produto[coluna], errors='coerce') 
# 'coerce' transforma valores inválidos em NaT


