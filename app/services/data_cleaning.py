import pandas as pd
import numpy as np

def tratar_itens_pedidos(path_csv: str):
    print(f"Iniciando tratamento de Itens: {path_csv}")
    
    # Lê o CSV direto do arquivo (Padrão JV)
    df = pd.read_csv(path_csv)

    # A. TRATAMENTO DE PREÇO E FRETE (12,34 -> 12.34)
    cols_valores = ['price', 'freight_value']
    
    for col in cols_valores:
        # Cria a coluna se não existir
        if col not in df.columns: 
            df[col] = np.nan
        
        # Se for texto, troca vírgula por ponto
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.replace(',', '.')

        # Converte para número (float)
        df[col] = pd.to_numeric(df[col], errors='coerce')

        # Preenche nulos com Mediana
        mediana = df[col].median()
        if pd.isna(mediana): mediana = 0.0
        df[col] = df[col].fillna(mediana)

    # B. TRATAMENTO DE DATA
    if 'shipping_limit_date' in df.columns:
        df['shipping_limit_date'] = pd.to_datetime(df['shipping_limit_date'], errors='coerce')

    return df