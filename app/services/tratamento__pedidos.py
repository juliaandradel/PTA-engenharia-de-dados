import pandas as pd
import numpy as np
from app.memory import valid_order_ids

def tratar_pedidos(dados: list):
    df = pd.DataFrame(dados)
    if df.empty: return []

    # Nível 1: Datas e Status
    cols_data = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]
    for col in cols_data:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    if "order_status" in df.columns:
        df["order_status"] = df["order_status"].astype(str).str.lower()
        mapa = {"delivered": "entregue", "invoiced": "faturado", "shipped": "enviado", "processing": "em processamento", "unavailable": "indisponível", "canceled": "cancelado", "created": "criado", "approved": "aprovado"}
        df["order_status"] = df["order_status"].replace(mapa)

    # Nível 1: Cálculo de Dias e Prazo
    if "order_delivered_customer_date" in df.columns and "order_purchase_timestamp" in df.columns:
        df["tempo_entrega_dias"] = (df["order_delivered_customer_date"] - df["order_purchase_timestamp"]).dt.days
        
    if "order_estimated_delivery_date" in df.columns and "order_purchase_timestamp" in df.columns:
        df["tempo_entrega_estimado_dias"] = (df["order_estimated_delivery_date"] - df["order_purchase_timestamp"]).dt.days

    if "tempo_entrega_dias" in df.columns and "tempo_entrega_estimado_dias" in df.columns:
        df["diferenca_entrega_dias"] = df["tempo_entrega_dias"] - df["tempo_entrega_estimado_dias"]
        df["entrega_no_prazo"] = df.apply(lambda x: "Não Entregue" if pd.isna(x["tempo_entrega_dias"]) else ("Sim" if x["diferenca_entrega_dias"] <= 0 else "Não"), axis=1)

    # Converter datas para string (Requisito JSON)
    for col in cols_data:
        if col in df.columns: df[col] = df[col].astype(str).replace('NaT', None)

    # Nível 2: Salvar na Memória
    if 'order_id' in df.columns:
        ids = set(df['order_id'].astype(str).unique())
        valid_order_ids.update(ids)
        print(f"💾 Memória: {len(ids)} Pedidos carregados.")

    df = df.replace({np.nan: None})
    return df.to_dict("records")