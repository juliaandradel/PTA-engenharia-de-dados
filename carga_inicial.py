import pandas as pd
import json
# Importando suas funções de limpeza existentes
from app.services.tratamento__produtos import clean_products
from app.services.tratamento__vendedores import clean_sellers
from app.services.tratamento__pedidos import tratar_pedidos
from app.services.tratamento__itens__pedidos import tratar_itens_pedidos

def rodar_carga_inicial():
    print("🚀 INICIANDO CARGA INICIAL (PROCESSAMENTO LOCAL)...")

    # --- 1. PRODUTOS ---
    print("\n📦 Processando Produtos...")
    try:
        # Ler
        df_prod = pd.read_csv("data/produtos.csv")
        # Converter para formato que a função aceita (Lista de Dicts)
        dados_brutos = df_prod.to_dict("records")
        # Limpar
        dados_limpos = clean_products(dados_brutos)
        # Salvar
        pd.DataFrame(dados_limpos).to_csv("data/produtos_tratados.csv", index=False)
        print(f"✅ Produtos salvos: {len(dados_limpos)} linhas.")
    except Exception as e:
        print(f"❌ Erro em Produtos: {e}")

    # --- 2. VENDEDORES ---
    print("\n👤 Processando Vendedores...")
    try:
        df_vend = pd.read_csv("data/vendedores.csv")
        dados_brutos = df_vend.to_dict("records")
        dados_limpos = clean_sellers(dados_brutos)
        pd.DataFrame(dados_limpos).to_csv("data/vendedores_tratados.csv", index=False)
        print(f"✅ Vendedores salvos: {len(dados_limpos)} linhas.")
    except Exception as e:
        print(f"❌ Erro em Vendedores: {e}")

    # --- 3. PEDIDOS ---
    print("\n📦 Processando Pedidos...")
    try:
        df_ped = pd.read_csv("data/pedidos.csv")
        dados_brutos = df_ped.to_dict("records")
        dados_limpos = tratar_pedidos(dados_brutos)
        pd.DataFrame(dados_limpos).to_csv("data/pedidos_tratados.csv", index=False)
        print(f"✅ Pedidos salvos: {len(dados_limpos)} linhas.")
    except Exception as e:
        print(f"❌ Erro em Pedidos: {e}")

    # --- 4. ITENS (O mais pesado) ---
    print("\n🛒 Processando Itens (com Integridade)...")
    try:
        df_itens = pd.read_csv("data/itens_pedidos.csv")
        dados_brutos = df_itens.to_dict("records")
        
        # A sua função de itens já lê os arquivos da pasta data/ para validar integridade
        # Como acabamos de salvar os arquivos originais lá, vai funcionar.
        dados_limpos = tratar_itens_pedidos(dados_brutos)
        
        pd.DataFrame(dados_limpos).to_csv("data/itens_pedidos_tratados.csv", index=False)
        print(f"✅ Itens salvos: {len(dados_limpos)} linhas.")
    except Exception as e:
        print(f"❌ Erro em Itens: {e}")

    print("\n🏁 CARGA INICIAL CONCLUÍDA! Arquivos '_tratados.csv' gerados na pasta data/.")

if __name__ == "__main__":
    rodar_carga_inicial()python carga_inicial.py