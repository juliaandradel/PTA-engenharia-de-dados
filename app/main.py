from fastapi import FastAPI
from app.services.tratamento__itens__pedidos import tratar_itens_pedidos
import uvicorn
from app.services.tratamento__vendedores import clean_sellers
from app.routers import example_router
from app.services.tratamento__produtos import clean_products
from app.services.tratamento__pedidos import tratar_pedidos




path_orders = "data/[Júlia] DataLake - pedidos.csv"
path_products = "data/[Júlia] DataLake - produtos.csv"
path_sellers = "data/[Júlia] DataLake - vendedores.csv"



app = FastAPI(title="API O-Market - Tratamento de Itens")

@app.get("/")
def read_root():
    return {"status": "API Online 🚀"}

@app.get("/health", description="Verifica a saúde da API.")
async def health_check():
    return {"status": "ok"}

@app.get("/pedidos-tratados", description="Retorna base de pedidos tratada.")
async def get_pedidos_tratados():

    df_tratado = tratar_pedidos(path_orders)
    return df_tratado.head(10).to_dict(orient="records")

app.include_router(example_router, prefix="/example", tags=["Example"])

@app.get("/vendedores-tratados", description="Retorna base de vendedores tratada.")
async def get_vendedores_tratados():
    # Indico o caminho do arquivo CSV como parâmetro
    df_tratado = clean_sellers(path_sellers)
    # Retorno as primeiras 10 linhas para facilitar o teste e evitar sobrecarga
    return df_tratado.head(10).to_dict(orient="records")

@app.get("/produtos-tratados", description="Retorna base de produtos tratada.")
async def get_produtos_tratados():
    df_tratado = clean_products(path_products)
    # Limita para as primeiras 10 linhas, igual ao endpoint de pedidos
    return df_tratado.head(10).to_dict(orient="records")

# --- ROTA GET PARA ITENS PEDIDOS ---
@app.get("/clean/items")
def get_clean_items(arquivo: str = "[Júlia] DataLake - itens_pedidos.csv"):
    """
    Rota GET para limpar itens de pedidos.
    O arquivo deve estar dentro da pasta 'data/'.
    """
    path_csv = f"data/{arquivo}"
    try:
        # Chama a função de itens passando o caminho completo
        df_limpo = tratar_itens_pedidos(path_csv)
        # Retorna o JSON
        return df_limpo.head(10).to_dict("records")
    except Exception as e:
        return {"status": "error", "message": f"Erro ao ler {path_csv}: {str(e)}"}

app.include_router(example_router, prefix="/example", tags=["Example"])