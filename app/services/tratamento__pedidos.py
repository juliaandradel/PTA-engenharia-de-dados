import pandas as pd
import numpy as np
from app.memory import valid_order_ids

def tratar_pedidos(dados: list):
    print("Iniciando Pedidos (Limpeza + Memória)...")
    df_pedido = pd.DataFrame(dados)
    if df_pedido.empty: return []

    # --- TRATAMENTO DE DADOS ---

    # 1. Conversão de Colunas de Data
    colunas_data = [
        "order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date",
        "order_delivered_customer_date", "order_estimated_delivery_date"
    ]
    
    # Converte para datetime para poder fazer contas
    for col in colunas_data:
        if col in df_pedido.columns:
            df_pedido[col] = pd.to_datetime(df_pedido[col], errors='coerce')

    # 2. Tradução e Padronização de Status
    if "order_status" in df_pedido.columns:
        df_pedido["order_status"] = df_pedido["order_status"].astype(str).str.lower()
        mapeamento = {
            "delivered": "entregue", "invoiced": "faturado", "shipped": "enviado",
            "processing": "em processamento", "unavailable": "indisponível",
            "canceled": "cancelado", "created": "criado", "approved": "aprovado"
        }
        df_pedido["order_status"] = df_pedido["order_status"].replace(mapeamento) 

    # 3. CÁLCULOS DE DIAS (A parte que faltava!)
    # Tempo real de entrega (Entrega - Compra)
    if "order_delivered_customer_date" in df_pedido.columns and "order_purchase_timestamp" in df_pedido.columns:
        df_pedido["tempo_entrega_dias"] = (df_pedido["order_delivered_customer_date"] - df_pedido["order_purchase_timestamp"]).dt.days

    # Tempo estimado (Estimativa - Compra)
    if "order_estimated_delivery_date" in df_pedido.columns and "order_purchase_timestamp" in df_pedido.columns:
        df_pedido["tempo_entrega_estimado_dias"] = (df_pedido["order_estimated_delivery_date"] - df_pedido["order_purchase_timestamp"]).dt.days

    # Diferença e Status de Prazo
    if "tempo_entrega_dias" in df_pedido.columns and "tempo_entrega_estimado_dias" in df_pedido.columns:
        df_pedido["diferenca_entrega_dias"] = df_pedido["tempo_entrega_dias"] - df_pedido["tempo_entrega_estimado_dias"]

        def check_prazo(row):
            if pd.isna(row.get("tempo_entrega_dias")): return "Não Entregue"
            if pd.isna(row.get("diferenca_entrega_dias")): return "Indefinido"
            return "Sim" if row["diferenca_entrega_dias"] <= 0 else "Não"

        df_pedido["entrega_no_prazo"] = df_pedido.apply(check_prazo, axis=1)

    # 4. Converter Datas para String (Para o JSON não quebrar na volta)
    for col in colunas_data:
        if col in df_pedido.columns:
            df_pedido[col] = df_pedido[col].astype(str).replace('NaT', None)

    # --- GESTÃO DE MEMÓRIA ---
    if 'order_id' in df_pedido.columns:
        ids_unicos = set(df_pedido['order_id'].astype(str).unique())
        valid_order_ids.update(ids_unicos)
        print(f"💾 {len(ids_unicos)} Pedidos salvos na memória.")

    df_pedido = df_pedido.replace({np.nan: None})
    return df_pedido.to_dict("records")