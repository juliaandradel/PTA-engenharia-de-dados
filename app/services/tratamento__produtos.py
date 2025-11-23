import pandas as pd
import numpy as np

def clean_products(dados: list):
    df = pd.DataFrame(dados)
    if df.empty: return []

    # 1. INTEGRIDADE
    try:
        df_itens = pd.read_csv("data/itens_pedidos.csv", usecols=['product_id'])
        df = df[df['product_id'].isin(df_itens['product_id'])]
    except FileNotFoundError:
        pass

    # 2. LIMPEZA
    if 'product_category_name' not in df.columns: df['product_category_name'] = 'indefinido'
    df['product_category_name'] = df['product_category_name'].fillna('indefinido').astype(str).str.lower().str.strip().str.replace(' ', '_')

    cols_num = ['product_name_lenght', 'product_description_lenght', 'product_photos_qty', 'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']
    for col in cols_num:
        if col not in df.columns: df[col] = np.nan
        df[col] = pd.to_numeric(df[col], errors='coerce')
        mediana = df[col].median()
        if pd.isna(mediana): mediana = 0
        df[col] = df[col].fillna(mediana)

    df = df.replace({np.nan: None})
    return df.to_dict("records")