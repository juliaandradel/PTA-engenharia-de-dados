from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any
from app.services.tratamento__itens__pedidos import tratar_itens_pedidos
from app.services.tratamento__vendedores import clean_sellers
from app.services.tratamento__produtos import clean_products
from app.services.tratamento__pedidos import tratar_pedidos
from app.memory import clear_memory

app = FastAPI(title="API O-Market - Protocolo Oficial")

@app.post("/reset-memory")
def reset_mem():
    clear_memory()
    return {"status": "Memória Limpa"}

@app.post("/produtos-tratados")
def prod(payload: List[Dict[str, Any]]):
    return clean_products(payload)

@app.post("/vendedores-tratados")
def vend(payload: List[Dict[str, Any]]):
    return clean_sellers(payload)

@app.post("/pedidos-tratados")
def ped(payload: List[Dict[str, Any]]):
    return tratar_pedidos(payload)

@app.post("/clean/items")
def item(payload: List[Dict[str, Any]]):
    return tratar_itens_pedidos(payload)