import pandas as pd
import numpy as np

def tratar_itens_pedidos(dados: list):
    """
    Limpa itens e valida integridade lendo os 3 arquivos 'Gabarito' da pasta data/.
    """
    print("Iniciando Itens (Validando contra ARQUIVOS LOCAIS de Pedidos, Produtos e Vendedores)...")
    
    # 1. Cria o DataFrame com o dado que chegou do n8n
    df_itens = pd.DataFrame(dados)
    if df_itens.empty: return []

    # 2. CARREGA GABARITO (Lê os CSVs tratados da pasta data)
    try:
        # Carrega IDs de PEDIDOS
        ids_orders = pd.read_csv("data/pedidos.csv", usecols=['order_id'])['order_id'].astype(str).unique()
        
        # Carrega IDs de PRODUTOS
        ids_products = pd.read_csv("data/produtos.csv", usecols=['product_id'])['product_id'].astype(str).unique()
        
        # Carrega IDs de VENDEDORES
        ids_sellers = pd.read_csv("data/vendedores.csv", usecols=['seller_id'])['seller_id'].astype(str).unique()
        
        # Transforma em SET (busca instantânea)
        set_orders = set(ids_orders)
        set_products = set(ids_products)
        set_sellers = set(ids_sellers)

    except FileNotFoundError as e:
        print(f"⚠️ Aviso: Arquivo de referência não encontrado ({e}). Pulando validação de integridade.")
        # Se não achar os arquivos, cria sets com os próprios dados para não apagar tudo (modo de segurança)
        set_orders = set(df_itens['order_id'].astype(str))
        set_products = set(df_itens['product_id'].astype(str))
        set_sellers = set(df_itens['seller_id'].astype(str))

    # 3. FILTRO DE INTEGRIDADE (Os 3 Pais)
    qtd_antes = len(df_itens)
    
    df_itens = df_itens[
        df_itens['order_id'].astype(str).isin(set_orders) &      # Checa Pedido
        df_itens['product_id'].astype(str).isin(set_products) &  # Checa Produto
        df_itens['seller_id'].astype(str).isin(set_sellers)      # Checa Vendedor
    ]
    
    print(f"✂️ Registros órfãos removidos: {qtd_antes - len(df_itens)}")

    # 4. LIMPEZA DE VALORES
    cols_valores = ['price', 'freight_value']
    for col in cols_valores:
        if col not in df_itens.columns: df_itens[col] = np.nan
        
        if df_itens[col].dtype == 'object':
            df_itens[col] = df_itens[col].astype(str).str.replace(',', '.')

        df_itens[col] = pd.to_numeric(df_itens[col], errors='coerce')
        
        mediana = df_itens[col].median()
        if pd.isna(mediana): mediana = 0.0
        df_itens[col] = df_itens[col].fillna(mediana)

    # 5. DATAS
    if 'shipping_limit_date' in df_itens.columns:
        df_itens['shipping_limit_date'] = pd.to_datetime(df_itens['shipping_limit_date'], errors='coerce')
        df_itens['shipping_limit_date'] = df_itens['shipping_limit_date'].astype(str).replace('NaT', None)

    df_itens = df_itens.replace({np.nan: None})
    return df_itens.to_dict("records")