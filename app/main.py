from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any

# Imports
from app.services.tratamento__itens__pedidos import tratar_itens_pedidos
from app.services.tratamento__vendedores import clean_sellers
from app.services.tratamento__produtos import clean_products
from app.services.tratamento__pedidos import tratar_pedidos

app = FastAPI(title="API O-Market (POST + Integridade)")

@app.get("/")
def read_root():
    return {"status": "API Online 🚀"}

# --- ROTAS POST (Recebem JSON, mas validam IDs localmente) ---

@app.post("/clean/items")
def post_clean_items(payload: List[Dict[str, Any]]):
    try:
        # A função tratar_itens_pedidos vai ler os CSVs locais para validar integridade
        return tratar_itens_pedidos(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clean/orders")
def post_clean_orders(payload: List[Dict[str, Any]]):
    try:
        return tratar_pedidos(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clean/products")
def post_clean_products(payload: List[Dict[str, Any]]):
    try:
        return clean_products(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clean/sellers")
def post_clean_sellers(payload: List[Dict[str, Any]]):
    try:
        return clean_sellers(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))