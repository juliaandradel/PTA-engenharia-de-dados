import pandas as pd
import numpy as np



    
# --- SUA LÓGICA (PRODUTOS) ---
def clean_products(path_csv:str):
    
    """
    Sua lógica de limpeza de produtos.
    """
    df = pd.read_csv(path_csv)

    # 1. Categoria (Texto)
    if 'product_category_name' not in df.columns:
        df['product_category_name'] = 'indefinido'
    
    df['product_category_name'] = df['product_category_name'].fillna('indefinido')
    
    df['product_category_name'] = (
        df['product_category_name']
        .astype(str)
        .str.lower()
        .str.strip()
        .str.replace(' ', '_')
    )

    # 2. Numéricos (Mediana)
    cols_numericas = [
        'product_name_lenght', 'product_description_lenght', 'product_photos_qty',
        'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm'
    ]

    for col in cols_numericas:
        if col not in df.columns:
            df[col] = np.nan
        
        df[col] = pd.to_numeric(df[col], errors='coerce')
        mediana = df[col].median()
        if pd.isna(mediana): mediana = 0
        df[col] = df[col].fillna(mediana)

    return df

