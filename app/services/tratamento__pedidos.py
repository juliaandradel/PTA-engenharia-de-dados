import pandas as pd
import numpy as np

class DataCleaning:
    
    # --- LÓGICA(PEDIDOS) ---
    def clean_orders(self, orders_list: list):
        """
        Lógica de tratamento de Pedidos (Adaptada para receber lista da API)
        """
        if not orders_list:
            return []
            
        # 1. Carregar DataFrame (Vem da lista da API, não do CSV)
        df_produto = pd.DataFrame(orders_list)

        # Lista de colunas para ajustar data/hora
        colunas_data = [
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ]

        # Blindagem: Cria colunas se não existirem (para não dar erro)
        for col in colunas_data + ["order_status"]:
            if col not in df_produto.columns:
                df_produto[col] = None

        # Converter todas as colunas para datetime
        for coluna in colunas_data:
            df_produto[coluna] = pd.to_datetime(df_produto[coluna], errors='coerce') 

        # Padroniza para minúscula
        df_produto["order_status"] = df_produto["order_status"].astype(str).str.lower()

        # Faz o mapeamento para português
        mapeamento_status = {
            "delivered": "entregue", "invoiced": "faturado", "shipped": "enviado",
            "processing": "em processamento", "unavailable": "indisponível",
            "canceled": "cancelado", "created": "criado", "approved": "aprovado"
        }

        # Substituição feita utilizando o dicionário
        df_produto["order_status"] = df_produto["order_status"].replace(mapeamento_status) 

        # Cálculos de dias
        df_produto["tempo_entrega_dias"] = (df_produto["order_delivered_customer_date"] - df_produto["order_purchase_timestamp"]).dt.days
        df_produto["tempo_entrega_estimado_dias"] = (df_produto["order_estimated_delivery_date"] - df_produto["order_purchase_timestamp"]).dt.days
        df_produto["diferenca_entrega_dias"] = df_produto["tempo_entrega_dias"] - df_produto["tempo_entrega_estimado_dias"]

        # Regra: entrega_no_prazo
        df_produto["entrega_no_prazo"] = df_produto.apply(
            lambda row: "Não Entregue" if pd.isna(row["tempo_entrega_dias"])
            else ("Sim" if row["diferenca_entrega_dias"] <= 0 else "Não"),
            axis=1
        )

        # Conversão para Int64 (para permitir nulos sem virar float)
        cols_int = ["tempo_entrega_dias", "tempo_entrega_estimado_dias", "diferenca_entrega_dias"]
        for col in cols_int:
            df_produto[col] = df_produto[col].astype("Int64")
            
        # CONVERSÃO FINAL: DataFrame -> Lista de Dicionários (JSON)
        # Importante: Converter datas para string para o JSON não quebrar
        for col in colunas_data:
            df_produto[col] = df_produto[col].astype(str).replace('NaT', None)
            
        return df_produto.to_dict("records")

    # --- SUA LÓGICA (PRODUTOS) ---
    def clean_products(self, products_list: list):
        """
        Sua lógica de limpeza de produtos.
        """
        if not products_list:
            return []
        
        df = pd.DataFrame(products_list)

        # 1. Categoria (Texto)
        if 'product_category_name' not in df.columns:
            df['product_category_name'] = 'indefinido'
        
        df['product_category_name'] = df['product_category_name'].fillna('indefinido')
        
        df['product_category_name'] = (
            df['product_category_name']
            .astype(str)
            .str.lower()
            .str.strip()
            .str.replace(' ', '_')
        )

        # 2. Numéricos (Mediana)
        cols_numericas = [
            'product_name_lenght', 'product_description_lenght', 'product_photos_qty',
            'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm'
        ]

        for col in cols_numericas:
            if col not in df.columns:
                df[col] = np.nan
            
            df[col] = pd.to_numeric(df[col], errors='coerce')
            mediana = df[col].median()
            if pd.isna(mediana): mediana = 0
            df[col] = df[col].fillna(mediana)

        return df.to_dict("records")

    # --- FUNÇÃO MESTRA (ORQUESTRADOR) ---
    def clean_all_data(self, payload):
        """
        Função que recebe o payload completo do main.py e distribui as tarefas.
        """
        return {
            "orders": self.clean_orders(payload.orders),       
            "products": self.clean_products(payload.products), 
            "order_items": payload.order_items,                # Passa direto 
            "sellers": payload.sellers                         # Passa direto
        }