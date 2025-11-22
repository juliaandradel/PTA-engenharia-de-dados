import pandas as pd
import numpy as np

def clean_products(path_csv: str, path_itens: str):
    """
    Trata produtos e remove aqueles que nunca foram vendidos (não estão em itens).
    """
    print(f"Iniciando tratamento de Produtos com validação de Vendas...")
    df = pd.read_csv(path_csv)

    # 1. Validação com Itens
    try:
        df_itens = pd.read_csv(path_itens, usecols=['product_id'])
        
        # FILTRO: Mantém apenas produtos presentes nos itens vendidos
        qtd_antes = len(df)
        df = df[df['product_id'].isin(df_itens['product_id'])]
        print(f"Produtos não vendidos removidos: {qtd_antes - len(df)}")
        
    except FileNotFoundError:
        print("Aviso: Arquivo de itens não encontrado. Pulando validação cruzada.")

    # --- Lógica original de limpeza ---
    if 'product_category_name' not in df.columns:
        df['product_category_name'] = 'indefinido'
    
    df['product_category_name'] = df['product_category_name'].fillna('indefinido')
    
    df['product_category_name'] = (
        df['product_category_name']
        .astype(str).str.lower().str.strip().str.replace(' ', '_')
    )

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

    return df