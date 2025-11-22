import pandas as pd
from unidecode import unidecode

def clean_sellers(path_csv: str, path_itens: str):
    """
    Trata vendedores e remove aqueles que não realizaram vendas.
    """
    print(f"Iniciando tratamento de Vendedores com validação de Vendas...")
    df = pd.read_csv(path_csv)

    # 1. Validação com Itens
    try:
        df_itens = pd.read_csv(path_itens, usecols=['seller_id'])
        
        # FILTRO: Mantém apenas vendedores presentes nos itens vendidos
        qtd_antes = len(df)
        df = df[df['seller_id'].isin(df_itens['seller_id'])]
        print(f"Vendedores inativos removidos: {qtd_antes - len(df)}")
        
    except FileNotFoundError:
        print("Aviso: Arquivo de itens não encontrado. Pulando validação cruzada.")

    # --- Lógica original de limpeza ---
    if 'seller_city' in df.columns:
        df['seller_city'] = (
            df['seller_city'].astype(str).apply(lambda x: unidecode(x).upper())
        )

    if 'seller_state' in df.columns:
        df['seller_state'] = df['seller_state'].astype(str).str.upper()

    return df