import pandas as pd
import numpy as np

def tratar_pedidos(path_csv: str, path_itens: str):
    """
    Trata pedidos e remove aqueles que não possuem itens associados.
    """
    print(f"Iniciando tratamento de Pedidos com validação de Itens...")
    
    # 1. Carregar Pedidos
    df_pedido = pd.read_csv(path_csv)

    # 2. Carregar Itens (Apenas ID para validar)
    try:
        df_itens = pd.read_csv(path_itens, usecols=['order_id'])
        
        # FILTRO: Mantém apenas pedidos que existem na tabela de itens
        qtd_antes = len(df_pedido)
        df_pedido = df_pedido[df_pedido['order_id'].isin(df_itens['order_id'])]
        print(f"Pedidos vazios (sem itens) removidos: {qtd_antes - len(df_pedido)}")
        
    except FileNotFoundError:
        print("Aviso: Arquivo de itens não encontrado. Pulando validação cruzada.")

    # --- Lógica original de limpeza ---
    colunas_data = [
        "order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date",
        "order_delivered_customer_date", "order_estimated_delivery_date"
    ]

    for coluna in colunas_data:
        if coluna in df_pedido.columns:
            df_pedido[coluna] = pd.to_datetime(df_pedido[coluna], errors='coerce') 

    if "order_status" in df_pedido.columns:
        df_pedido["order_status"] = df_pedido["order_status"].str.lower()
        mapeamento_status = {
            "delivered": "entregue", "invoiced": "faturado", "shipped": "enviado",
            "processing": "em processamento", "unavailable": "indisponível",
            "canceled": "cancelado", "created": "criado", "approved": "aprovado"
        }
        df_pedido["order_status"] = df_pedido["order_status"].replace(mapeamento_status) 

    # Cálculos de datas (mantendo a lógica original)
    if "order_delivered_customer_date" in df_pedido.columns and "order_purchase_timestamp" in df_pedido.columns:
        df_pedido["tempo_entrega_dias"] = (df_pedido["order_delivered_customer_date"] - df_pedido["order_purchase_timestamp"]).dt.days

    if "order_estimated_delivery_date" in df_pedido.columns and "order_purchase_timestamp" in df_pedido.columns:
        df_pedido["tempo_entrega_estimado_dias"] = (df_pedido["order_estimated_delivery_date"] - df_pedido["order_purchase_timestamp"]).dt.days

    if "tempo_entrega_dias" in df_pedido.columns and "tempo_entrega_estimado_dias" in df_pedido.columns:
        df_pedido["diferenca_entrega_dias"] = df_pedido["tempo_entrega_dias"] - df_pedido["tempo_entrega_estimado_dias"]

        df_pedido["entrega_no_prazo"] = df_pedido.apply(
            lambda row: "Não Entregue" if pd.isna(row["tempo_entrega_dias"])
            else ("Sim" if row["diferenca_entrega_dias"] <= 0 else "Não"),
            axis=1 
        )
        
        # Conversão para Int64 para aceitar nulos
        cols_int = ["tempo_entrega_dias", "tempo_entrega_estimado_dias", "diferenca_entrega_dias"]
        for col in cols_int:
            if col in df_pedido.columns:
                df_pedido[col] = df_pedido[col].astype("Int64")

    return df_pedido