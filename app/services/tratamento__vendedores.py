import pandas as pd
import unidecode  # Instale com: pip install unidecode

def clean_sellers(path_csv: str):
    # Carrego a planilha usando pandas.
    df = pd.read_csv(path_csv)

    # Padronizo o nome da cidade dos vendedores.
    # Tiro os acentos e deixo tudo em maiúsculas.
    if 'seller_city' in df.columns:
        df['seller_city'] = (
            df['seller_city']
            .astype(str)  # Confirma que é texto
            .apply(lambda x: unidecode.unidecode(x).upper())  # Remove acentos e coloca em caixa alta
        )

    # Padronizo o estado (UF) também para caixa alta (ex: 'sp' vira 'SP').
    if 'seller_state' in df.columns:
        df['seller_state'] = (
            df['seller_state']
            .astype(str)
            .str.upper()
        )

    # Retorno o DataFrame pronto para usar.
    return df
