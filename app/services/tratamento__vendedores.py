import pandas as pd
from unidecode import unidecode
from app.memory import valid_seller_ids

def clean_sellers(dados: list):
    df = pd.DataFrame(dados)
    if df.empty: return []

    # Nível 1: Geografia
    if 'seller_city' in df.columns:
        df['seller_city'] = df['seller_city'].astype(str).apply(lambda x: unidecode(x).upper())
    if 'seller_state' in df.columns:
        df['seller_state'] = df['seller_state'].astype(str).str.upper()

    # Nível 2: Salvar na Memória
    if 'seller_id' in df.columns:
        ids = set(df['seller_id'].astype(str).unique())
        valid_seller_ids.update(ids)
        print(f"💾 Memória: {len(ids)} Vendedores carregados.")

    df = df.replace({float('nan'): None})
    return df.to_dict("records")