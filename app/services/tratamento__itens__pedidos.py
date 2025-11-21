
import pandas as pd
import numpy as np

def tratar_itens_pedidos(path_itens: str, path_orders: str, path_products: str, path_sellers: str):
    """
    Limpa itens de pedidos e remove registros órfãos (IDs que não existem nas outras tabelas).
    """
    print(f"Iniciando tratamento de Itens com Integridade...")
    
    # 1. Carregar a tabela principal
    try:
        df_itens = pd.read_csv(path_itens)
    except FileNotFoundError:
        print(f"Erro: Arquivo {path_itens} não encontrado.")
        return pd.DataFrame()

    # 2. Carregar tabelas pai (Só os IDs para ser rápido)
    print("Carregando referências...")
    try:
        df_orders = pd.read_csv(path_orders, usecols=['order_id'])
        df_products = pd.read_csv(path_products, usecols=['product_id'])
        df_sellers = pd.read_csv(path_sellers, usecols=['seller_id'])
    except FileNotFoundError as e:
        print(f"Erro ao carregar referências: {e}")
        return pd.DataFrame()

    # 3. FILTRO DE INTEGRIDADE (O Pulo do Gato)
    qtd_antes = len(df_itens)
    
    # Mantém só o que tem par
    df_itens = df_itens[df_itens['order_id'].isin(df_orders['order_id'])]
    df_itens = df_itens[df_itens['product_id'].isin(df_products['product_id'])]
    df_itens = df_itens[df_itens['seller_id'].isin(df_sellers['seller_id'])]

    print(f"Linhas removidas (órfãs): {qtd_antes - len(df_itens)}")

    # 4. LIMPEZA DE DADOS (Sua lógica original)
    cols_valores = ['price', 'freight_value']
    for col in cols_valores:
        if col not in df_itens.columns: df_itens[col] = np.nan
        
        # Vírgula -> Ponto
        if df_itens[col].dtype == 'object':
            df_itens[col] = df_itens[col].astype(str).str.replace(',', '.')

        # Float
        df_itens[col] = pd.to_numeric(df_itens[col], errors='coerce')

        # Mediana
        mediana = df_itens[col].median()
        if pd.isna(mediana): mediana = 0.0
        df_itens[col] = df_itens[col].fillna(mediana)

    # 5. DATAS
    if 'shipping_limit_date' in df_itens.columns:
        df_itens['shipping_limit_date'] = pd.to_datetime(df_itens['shipping_limit_date'], errors='coerce')

    return df_itens