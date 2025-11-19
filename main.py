import pandas as pd
from src.sellers_cleaning import SellerCleaning

# Configurações
ARQUIVO_ENTRADA = 'vendedores.csv'
ARQUIVO_SAIDA = 'vendedores_tratados.csv'

def main():
    try:
        # 1. Ler CSV
        print(f"Lendo arquivo: {ARQUIVO_ENTRADA}")
        df = pd.read_csv(ARQUIVO_ENTRADA)

        # 2. Instanciar a classe de limpeza de VENDEDORES
        cleaner = SellerCleaning()
        
        # 3. Executar a limpeza
        df_tratado = cleaner.clean_sellers(df)

        # 4. Salvar
        print(f"Salvando em: {ARQUIVO_SAIDA}")
        df_tratado.to_csv(ARQUIVO_SAIDA, index=False)
        print("Sucesso! Vendedores tratados. 🚀")

    except FileNotFoundError:
        print(f"ERRO: O arquivo '{ARQUIVO_ENTRADA}' não foi encontrado. Verifique o nome!")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()