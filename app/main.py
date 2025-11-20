from fastapi import FastAPI
import uvicorn
from app.services.tratamento__vendedores import clean_sellers
from app.routers import example_router

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

@app.get("/vendedores-tratados", description="Retorna base de vendedores tratada.")
async def get_vendedores_tratados():
    # Indico o caminho do arquivo CSV como parâmetro
    caminho_csv = "/app/data/[Júlia] DataLake - vendedores.csv"
    df_tratado = clean_sellers(caminho_csv)
    # Retorno as primeiras 10 linhas para facilitar o teste e evitar sobrecarga
    return df_tratado.head(10).to_dict(orient="records")

app.include_router(example_router, prefix="/example", tags=["Example"])