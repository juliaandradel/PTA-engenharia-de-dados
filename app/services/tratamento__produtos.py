import pandas as pd
import numpy as np
from app.memory import valid_product_ids

def clean_products(dados: list):
    print("Iniciando Produtos (Limpeza + Memória)...")
    df = pd.DataFrame(dados)
    if df.empty: return []

    # --- TRATAMENTO DE DADOS ---
    
    # 1. Categoria (Texto): Lowercase, strip, snake_case e preenche nulos
    if 'product_category_name' not in df.columns:
        df['product_category_name'] = 'indefinido'
    
    df['product_category_name'] = df['product_category_name'].fillna('indefinido')
    df['product_category_name'] = (
        df['product_category_name'].astype(str)
        .str.lower()
        .str.strip()
        .str.replace(' ', '_')
    )

    # 2. Numéricos: Converte para número e preenche nulos com a Mediana
    cols_numericas = [
        'product_name_lenght', 'product_description_lenght', 'product_photos_qty',
        'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm'
    ]

    for col in cols_numericas:
        if col not in df.columns: df[col] = np.nan
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
        mediana = df[col].median()
        if pd.isna(mediana): mediana = 0
        
        df[col] = df[col].fillna(mediana)

    # --- GESTÃO DE MEMÓRIA ---
    if 'product_id' in df.columns:
        ids_unicos = set(df['product_id'].astype(str).unique())
        valid_product_ids.update(ids_unicos)
        print(f"💾 {len(ids_unicos)} Produtos salvos na memória.")

    # Blindagem final
    df = df.replace({np.nan: None})
    return df.to_dict("records")