from fastapi import FastAPI
from fastapi import Query
# Imports dos arquivos separados
from app.services.tratamento__itens__pedidos import tratar_itens_pedidos
from app.services.tratamento__vendedores import clean_sellers
from app.routers import example_router
from app.services.tratamento__produtos import clean_products
from app.services.tratamento__pedidos import tratar_pedidos

app = FastAPI(title="API O-Market - Tratamento de Dados Integrado")

@app.get("/")
def read_root():
    return {"status": "API Online 🚀"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# --- ROTA PEDIDOS (Agora exige itens para validar) ---
@app.get("/pedidos-tratados")
async def get_pedidos_tratados(
    arquivo: str = "[Júlia] DataLake - pedidos.csv",
    arquivo_itens: str = "[Júlia] DataLake - itens_pedidos.csv", # <--- Novo
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, le=100)
):
    path_orders = f"data/{arquivo}"
    path_items = f"data/{arquivo_itens}"
    try:
        # Passa os DOIS caminhos
        df_tratado = tratar_pedidos(path_orders, path_items)
        return df_tratado.iloc[skip:skip+limit].to_dict(orient="records")
    except Exception as e:
        return {"status": "error", "message": f"Erro ao processar pedidos: {str(e)}"}

# --- ROTA VENDEDORES (Agora exige itens para validar) ---
@app.get("/vendedores-tratados")
async def get_vendedores_tratados(
    arquivo: str = "[Júlia] DataLake - vendedores.csv",
    arquivo_itens: str = "[Júlia] DataLake - itens_pedidos.csv", # <--- Novo
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, le=100)
):
    path_sellers = f"data/{arquivo}"
    path_items = f"data/{arquivo_itens}"
    try:
        # Passa os DOIS caminhos
        df_tratado = clean_sellers(path_sellers, path_items)
        return df_tratado.iloc[skip:skip+limit].to_dict(orient="records")
    except Exception as e:
        return {"status": "error", "message": f"Erro ao processar vendedores: {str(e)}"}

# --- ROTA PRODUTOS (Agora exige itens para validar) ---
@app.get("/produtos-tratados")
async def get_produtos_tratados(
    arquivo: str = "[Júlia] DataLake - produtos.csv",
    arquivo_itens: str = "[Júlia] DataLake - itens_pedidos.csv", # <--- Novo
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, le=100)
):
    path_products = f"data/{arquivo}"
    path_items = f"data/{arquivo_itens}"
    try:
        # Passa os DOIS caminhos
        df_tratado = clean_products(path_products, path_items)
        return df_tratado.iloc[skip:skip+limit].to_dict(orient="records")
    except Exception as e:
        return {"status": "error", "message": f"Erro ao processar produtos: {str(e)}"}

# --- ROTA ITENS PEDIDOS 
@app.get("/clean/items")
def get_clean_items(
    arquivo_itens: str = "[Júlia] DataLake - itens_pedidos.csv",
    arquivo_pedidos: str = "[Júlia] DataLake - pedidos.csv",
    arquivo_produtos: str = "[Júlia] DataLake - produtos.csv",
    arquivo_vendedores: str = "[Júlia] DataLake - vendedores.csv",
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100)
):
    path_itens = f"data/{arquivo_itens}"
    path_orders = f"data/{arquivo_pedidos}"
    path_products = f"data/{arquivo_produtos}"
    path_sellers = f"data/{arquivo_vendedores}"

    try:
        # Chama a função passando os 4 caminhos
        df_limpo = tratar_itens_pedidos(path_itens, path_orders, path_products, path_sellers)
        return df_limpo.iloc[skip:skip+limit].to_dict("records")
    except Exception as e:
        return {"status": "error", "message": str(e)}

app.include_router(example_router, prefix="/example", tags=["Example"])