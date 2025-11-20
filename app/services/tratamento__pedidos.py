import  pandas as pd
import numpy as np


def tratar_pedidos(path_csv:str):
    
    #carregando o data frame 
    df_produto = pd.read_csv("/app/data/[Júlia] DataLake - pedidos.csv")

    #lista de colunas para ajustar data/hora antes da converção 
    colunas_data = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    # Converter todas as colunas para datetime
    for coluna in colunas_data:
        df_produto[coluna] = pd.to_datetime(df_produto[coluna], errors='coerce') 
    # 'coerce' transforma valores inválidos em NaT


    # padroniza para minúscula
    df_produto["order_status"] = df_produto["order_status"].str.lower()

    # faz o mapeamento para português
    mapeamento_status = {
        "delivered": "entregue",
        "invoiced": "faturado",
        "shipped": "enviado",
        "processing": "em processamento",
        "unavailable": "indisponível",
        "canceled": "cancelado",
        "created": "criado",
        "approved": "aprovado"
    }

    #substituição feita utilizando o dicionário
    df_produto["order_status"] = df_produto["order_status"].replace(mapeamento_status) 



    # order_delivered_customer_date (data de entrega)
    # order_purchase_timestamp (data de compra)
    # order_estimated_delivery_date (data estimada de entrega)

    # tempo_entrega_dias - diferença entre entrega e compra
    df_produto["tempo_entrega_dias"] = (df_produto["order_delivered_customer_date"] - df_produto["order_purchase_timestamp"]).dt.days
    #.dt.days serve para extrair a quantidade de dias de uma diferença entre datas por que é um objeto diferente se uma soma normal int no caso

    # tempo_entrega_estimado_dias - diferença entre estimativa e compra
    df_produto["tempo_entrega_estimado_dias"] = (df_produto["order_estimated_delivery_date"] - df_produto["order_purchase_timestamp"]).dt.days

    # diferenca_entrega_dias - tempo real menos estimado
    df_produto["diferenca_entrega_dias"] = df_produto["tempo_entrega_dias"] - df_produto["tempo_entrega_estimado_dias"]

    # usei o método .apply() para aplicar uma função em cada linha (axis=1)
    # entrega_no_prazo - "Sim" se diferenca_entrega_dias <= 0, "Não" se > 0, "Não Entregue" se tempo_entrega_dias está nulo
    df_produto["entrega_no_prazo"] = df_produto.apply(
        # usei a função lambda, que é uma função rápida, sem nome (anônima)
        # Cada 'row' representa uma linha do DataFrame
        lambda row: "Não Entregue" if pd.isna(row["tempo_entrega_dias"])
        else ("Sim" if row["diferenca_entrega_dias"] <= 0 else "Não"),
        axis=1 # axis=1 indica que a função será aplicada em cada linha
    )

    #algumas colunas de entrega tinham valores com ponto (pois tinham mudado para float, já que alguns valores estavam vazios nas colunas)
    # O tipo "Int64" do pandas permite valores nulos (NaN) mesmo na coluna inteira, sem precisar usar float. Com isso, os números inteiros vão aparecer sem ponto
    df_produto["tempo_entrega_dias"] = df_produto["tempo_entrega_dias"].astype("Int64") 
    df_produto["tempo_entrega_estimado_dias"] = df_produto["tempo_entrega_estimado_dias"].astype("Int64")
    df_produto["diferenca_entrega_dias"] = df_produto["diferenca_entrega_dias"].astype("Int64")


    return df_produto