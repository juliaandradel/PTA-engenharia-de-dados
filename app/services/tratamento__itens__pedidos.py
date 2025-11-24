import pandas as pd
import numpy as np
from app.memory import valid_order_ids, valid_product_ids, valid_seller_ids

def tratar_itens_pedidos(dados: list):
    print("Iniciando Itens (Validando contra Memória RAM)...")
    df_itens = pd.DataFrame(dados)
    if df_itens.empty: return []

    # --- 1. INTEGRIDADE REFERENCIAL (Filtro) ---
    qtd_antes = len(df_itens)
    
    # Só mantém se o ID estiver na memória
    df_itens = df_itens[
        df_itens['order_id'].astype(str).isin(valid_order_ids) &
        df_itens['product_id'].astype(str).isin(valid_product_ids) &
        df_itens['seller_id'].astype(str).isin(valid_seller_ids)
    ]
    
    print(f"✂️ Registros órfãos removidos: {qtd_antes - len(df_itens)}")

    # --- 2. TRATAMENTO DE DADOS ---

    # Preço e Frete (Vírgula -> Ponto)
    cols_valores = ['price', 'freight_value']
    for col in cols_valores:
        if col not in df_itens.columns: df_itens[col] = np.nan
        
        if df_itens[col].dtype == 'object':
            df_itens[col] = df_itens[col].astype(str).str.replace(',', '.')

        df_itens[col] = pd.to_numeric(df_itens[col], errors='coerce')
        
        mediana = df_itens[col].median()
        if pd.isna(mediana): mediana = 0.0
        df_itens[col] = df_itens[col].fillna(mediana)

    # Datas
    if 'shipping_limit_date' in df_itens.columns:
        df_itens['shipping_limit_date'] = pd.to_datetime(df_itens['shipping_limit_date'], errors='coerce')
        df_itens['shipping_limit_date'] = df_itens['shipping_limit_date'].astype(str).replace('NaT', None)

    df_itens = df_itens.replace({np.nan: None})
    return df_itens.to_dict("records")