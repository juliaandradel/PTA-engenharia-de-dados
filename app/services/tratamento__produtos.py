import pandas as pd
import numpy as np
from app.memory import valid_product_ids

def clean_products(dados: list):
    df = pd.DataFrame(dados)
    if df.empty: return []

    # Nível 1: Padronização
    if 'product_category_name' in df.columns:
        df['product_category_name'] = df['product_category_name'].fillna('indefinido').astype(str).str.lower().str.strip().str.replace(' ', '_')

    # Nível 1: Nulos numéricos
    cols_num = ['product_name_lenght', 'product_description_lenght', 'product_photos_qty', 'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']
    for col in cols_num:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(df[col].median() if not pd.isna(df[col].median()) else 0)

    # Nível 2: Salvar na Memória
    if 'product_id' in df.columns:
        ids = set(df['product_id'].astype(str).unique())
        valid_product_ids.update(ids)
        print(f"💾 Memória: {len(ids)} Produtos carregados.")

    df = df.replace({np.nan: None})
    return df.to_dict("records")