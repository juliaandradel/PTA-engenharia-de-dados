import pandas as pd
import numpy as np
from app.memory import valid_order_ids, valid_product_ids, valid_seller_ids

def tratar_itens_pedidos(dados: list):
    print("Iniciando Itens (Validando contra Memória RAM)...")
    
    # 1. Cria o DataFrame
    df = pd.DataFrame(dados)
    if df.empty: return []

    # --- 2. INTEGRIDADE REFERENCIAL (O Filtro) ---
    qtd_antes = len(df)
    
    # Filtra validando contra a memória (Sets globais)
    df = df[
        df['order_id'].astype(str).isin(valid_order_ids) &
        df['product_id'].astype(str).isin(valid_product_ids) &
        df['seller_id'].astype(str).isin(valid_seller_ids)
    ]
    
    print(f"✂️ Integridade: {qtd_antes - len(df)} órfãos removidos.")

    # --- 3. TRATAMENTO DE DADOS (Correção da Vírgula BLINDADA) ---
    cols_valores = ['price', 'freight_value']
    
    for col in cols_valores:
        # Garante que a coluna existe
        if col not in df.columns: 
            df[col] = np.nan
        

        df[col] = df[col].astype(str).str.replace(',', '.')

        # Agora converte para Float (Número real)
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Preenche vazios com a Mediana
        mediana = df[col].median()
        if pd.isna(mediana): mediana = 0.0
        df[col] = df[col].fillna(mediana)

    # 4. Datas
    if 'shipping_limit_date' in df.columns:
        df['shipping_limit_date'] = pd.to_datetime(df['shipping_limit_date'], errors='coerce')
        df['shipping_limit_date'] = df['shipping_limit_date'].astype(str).replace('NaT', None)

    # 5. Blindagem Final
    df = df.replace({np.nan: None})
    
    return df.to_dict("records")