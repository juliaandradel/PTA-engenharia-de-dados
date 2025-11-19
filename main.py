import pandas as pd
from src.data_cleaning import DataCleaning

def main():
    try:
        # 1. Ler
        print("Lendo produtos.csv...")
        df = pd.read_csv('produtos.csv')

        # 2. Limpar (Usando a Classe)
        cleaner = DataCleaning()
        df_limpo = cleaner.clean_products(df)

        # 3. Salvar
        print("Salvando produtos_tratados.csv...")
        df_limpo.to_csv('produtos_tratados.csv', index=False)
        print("Sucesso! 🚀")

    except FileNotFoundError:
        print("ERRO: Arquivo 'produtos.csv' não encontrado.")

if __name__ == "__main__":
    main()