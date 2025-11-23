import pandas as pd
from unidecode import unidecode
import numpy as np

def clean_sellers(dados: list):
    df = pd.DataFrame(dados)
    if df.empty: return []

    # 1. INTEGRIDADE
    try:
        df_itens = pd.read_csv("data/itens_pedidos.csv", usecols=['seller_id'])
        df = df[df['seller_id'].isin(df_itens['seller_id'])]
    except FileNotFoundError:
        pass

    # 2. LIMPEZA
    if 'seller_city' in df.columns:
        df['seller_city'] = df['seller_city'].astype(str).apply(lambda x: unidecode(x).upper())
    
    if 'seller_state' in df.columns:
        df['seller_state'] = df['seller_state'].astype(str).str.upper()

    df = df.replace({np.nan: None})
    return df.to_dict("records")