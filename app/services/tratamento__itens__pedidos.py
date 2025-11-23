import pandas as pd
import numpy as np

def tratar_itens_pedidos(dados: list):
    print("Iniciando tratamento de Itens (POST) com Integridade...")
    
    # 1. Transforma JSON recebido em DataFrame
    df_itens = pd.DataFrame(dados)
    if df_itens.empty: return []

    # 2. CARREGA REFERÊNCIAS (Lê do disco apenas para validar IDs)
    # Assumimos que a pasta data/ contém a "verdade absoluta" dos dados
    try:
        df_orders = pd.read_csv("data/pedidos.csv", usecols=['order_id'])
        df_products = pd.read_csv("data/produtos.csv", usecols=['product_id'])
        df_sellers = pd.read_csv("data/vendedores.csv", usecols=['seller_id'])
        
        # 3. FILTRO DE INTEGRIDADE (Remove órfãos)
        qtd_antes = len(df_itens)
        df_itens = df_itens[
            df_itens['order_id'].isin(df_orders['order_id']) &
            df_itens['product_id'].isin(df_products['product_id']) &
            df_itens['seller_id'].isin(df_sellers['seller_id'])
        ]
        print(f"Registros órfãos removidos: {qtd_antes - len(df_itens)}")
        
    except FileNotFoundError as e:
        print(f"⚠️ Aviso: Não foi possível carregar tabelas para validação: {e}")
        # Se não achar os arquivos, segue apenas com a limpeza de valores

    # 4. LIMPEZA DE VALORES (Vírgula e Datas)
    cols_valores = ['price', 'freight_value']
    for col in cols_valores:
        if col not in df_itens.columns: df_itens[col] = np.nan
        
        if df_itens[col].dtype == 'object':
            df_itens[col] = df_itens[col].astype(str).str.replace(',', '.')

        df_itens[col] = pd.to_numeric(df_itens[col], errors='coerce')
        
        mediana = df_itens[col].median()
        if pd.isna(mediana): mediana = 0.0
        df_itens[col] = df_itens[col].fillna(mediana)

    if 'shipping_limit_date' in df_itens.columns:
        df_itens['shipping_limit_date'] = pd.to_datetime(df_itens['shipping_limit_date'], errors='coerce')
        # Converte para string ISO para retorno JSON
        df_itens['shipping_limit_date'] = df_itens['shipping_limit_date'].astype(str).replace('NaT', None)

    # Blindagem para retorno
    df_itens = df_itens.replace({np.nan: None})

    return df_itens.to_dict("records")