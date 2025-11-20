from fastapi import FastAPI
import uvicorn
from app.routers import example_router
from app.services.tratamento__produtos import clean_products


app = FastAPI(
    title="API de Tratamento de Dados - Desafio 1",
    description="API que recebe dados brutos, os trata e os devolve limpos.",
    version="1.0.0"
)

@app.get("/", description="Mensagem de boas-vindas da API.")
async def read_root():
    return {"message": "Bem-vindo à API de Tratamento de Dados!"}

@app.get("/health", description="Verifica a saúde da API.")
async def health_check():
    return {"status": "ok"}

@app.get("/produtos-tratados", description="Retorna base de produtos tratada.")
async def get_produtos_tratados():
    caminho_csv = "/app/data/[Júlia] DataLake - produtos.csv"
    df_tratado = clean_products(caminho_csv)
    # Limita para as primeiras 10 linhas, igual ao endpoint de pedidos
    return df_tratado.head(10).to_dict(orient="records")

app.include_router(example_router, prefix="/example", tags=["Example"])

