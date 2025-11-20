from fastapi import FastAPI
from app.services.data_cleaning import tratar_itens_pedidos

app = FastAPI(title="API O-Market - Tratamento de Itens")

@app.get("/")
def read_root():
    return {"status": "API Online 🚀"}

# --- ROTA GET PARA ITENS PEDIDOS ---
@app.get("/clean/items")
def get_clean_items(arquivo: str = "itens_pedidos.csv"):
    """
    Rota GET para limpar itens de pedidos.
    O arquivo deve estar dentro da pasta 'data/'.
    """
   
    path_csv = f"data/{arquivo}"
    
    print(f"Buscando arquivo em: {path_csv}")

    try:
        # Chama a função de itens passando o caminho completo
        df_limpo = tratar_itens_pedidos(path_csv)
        # Retorna o JSON
        return df_limpo.to_dict("records")
    except Exception as e:
        return {"status": "error", "message": f"Erro ao ler {path_csv}: {str(e)}"}