import pandas as pd
import numpy as np
from unidecode import unidecode

class SellerCleaning:
    def clean_sellers(self, df):
        """
        Realiza o tratamento de dados da tabela de Vendedores.
        """
        print("Iniciando limpeza de Vendedores...")

        # Garante que as colunas existem
        colunas_texto = ['seller_city', 'seller_state']
        for col in colunas_texto:
            if col not in df.columns:
                df[col] = 'indefinido'
            df[col] = df[col].fillna('indefinido')

        # --- REGRA 1: CIDADE (Remove acento + Uppercase) ---
        # Ex: 'são paulo' -> 'SAO PAULO'
        def tratar_cidade(valor):
            valor_str = str(valor)
            sem_acento = unidecode(valor_str) # Remove ã, é, ç...
            return sem_acento.upper()         # Vira MAIÚSCULO

        df['seller_city'] = df['seller_city'].apply(tratar_cidade)

        # --- REGRA 2: ESTADO (Uppercase) ---
        # Ex: 'sp' -> 'SP'
        df['seller_state'] = df['seller_state'].astype(str).str.upper().str.strip()

        return df