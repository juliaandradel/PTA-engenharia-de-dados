import pandas as pd
import numpy as np

def tratar_itens_pedidos(path_csv: str):
    print(f"Iniciando tratamento de Itens: {path_csv}")
    
    # Lê o arquivo original
    df = pd.read_csv(path_csv)

    # --- REGRA 1: VALORES NUMÉRICOS (Price e Freight) ---
    cols_valores = ['price', 'freight_value']
    
    for col in cols_valores:
        # Garante que a coluna existe (blindagem)
        if col not in df.columns: 
            df[col] = np.nan
        
        # Troca VÍRGULA por PONTO (se for texto) para o Python entender
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.replace(',', '.')

        # Converte para número real (float)
        df[col] = pd.to_numeric(df[col], errors='coerce')

        # --- REGRA 2: TRATAMENTO DE NULOS (Mediana) ---
        mediana = df[col].median()
        
        # Se a mediana der nulo (tabela vazia), usa 0.0
        if pd.isna(mediana): 
            mediana = 0.0
            
        # Preenche os buracos com a mediana
        df[col] = df[col].fillna(mediana)

    # --- REGRA 3: DATAS (Shipping Limit) ---
    if 'shipping_limit_date' in df.columns:
        df['shipping_limit_date'] = pd.to_datetime(df['shipping_limit_date'], errors='coerce')

    return df