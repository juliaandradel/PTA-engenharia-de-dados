import pandas as pd
from unidecode import unidecode
from app.memory import valid_seller_ids

def clean_sellers(dados: list):
    print("Iniciando Vendedores (Limpeza + Memória)...")
    df = pd.DataFrame(dados)
    if df.empty: return []

    # --- TRATAMENTO DE DADOS ---

    # 1. Cidade: Remove acentos e coloca em MAIÚSCULO
    if 'seller_city' in df.columns:
        def tratar_texto(txt):
            if pd.isna(txt): return ""
            return unidecode(str(txt)).upper()
            
        df['seller_city'] = df['seller_city'].apply(tratar_texto)

    # 2. Estado: Coloca em MAIÚSCULO
    if 'seller_state' in df.columns:
        df['seller_state'] = df['seller_state'].astype(str).str.upper()

    # --- GESTÃO DE MEMÓRIA ---
    if 'seller_id' in df.columns:
        ids_unicos = set(df['seller_id'].astype(str).unique())
        valid_seller_ids.update(ids_unicos)
        print(f"💾 {len(ids_unicos)} Vendedores salvos na memória.")

    df = df.replace({float('nan'): None})
    return df.to_dict("records")