import pandas as pd
import numpy as np
from app.memory import valid_order_ids, valid_product_ids, valid_seller_ids

def tratar_itens_pedidos(dados: list):
    df = pd.DataFrame(dados)
    if df.empty: return []

    # Nível 2: Integridade (Regra dos Órfãos)
    qtd_antes = len(df)
    df = df[
        df['order_id'].astype(str).isin(valid_order_ids) &
        df['product_id'].astype(str).isin(valid_product_ids) &
        df['seller_id'].astype(str).isin(valid_seller_ids)
    ]
    print(f"✂️ Integridade: {qtd_antes - len(df)} órfãos removidos.")

    # Nível 1: Conversão Numérica (Vírgula -> Ponto)
    cols_val = ['price', 'freight_value']
    for col in cols_val:
        if col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.replace(',', '.')
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(df[col].median() if not pd.isna(df[col].median()) else 0)

    # Nível 1: Datas
    if 'shipping_limit_date' in df.columns:
        df['shipping_limit_date'] = pd.to_datetime(df['shipping_limit_date'], errors='coerce')
        df['shipping_limit_date'] = df['shipping_limit_date'].astype(str).replace('NaT', None)

    df = df.replace({np.nan: None})
    return df.to_dict("records")