from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any

# Imports
from app.services.tratamento__itens__pedidos import tratar_itens_pedidos
from app.services.tratamento__vendedores import clean_sellers
from app.services.tratamento__produtos import clean_products
from app.services.tratamento__pedidos import tratar_pedidos
from app.memory import clear_memory

app = FastAPI(title="API O-Market (Final)")

@app.get("/")
def read_root():
    return {"status": "API Online 🚀"}

# --- ROTA DE RESET (Início do n8n) ---
@app.post("/reset-memory")
def post_reset_memory():
    clear_memory()
    return {"status": "Memória limpa."}

# --- ROTAS DE TRATAMENTO (POST) ---
@app.post("/pedidos-tratados")
def post_pedidos(payload: List[Dict[str, Any]]):
    try: return tratar_pedidos(payload)
    except Exception as e: raise HTTPException(500, str(e))

@app.post("/produtos-tratados")
def post_produtos(payload: List[Dict[str, Any]]):
    try: return clean_products(payload)
    except Exception as e: raise HTTPException(500, str(e))

@app.post("/vendedores-tratados")
def post_vendedores(payload: List[Dict[str, Any]]):
    try: return clean_sellers(payload)
    except Exception as e: raise HTTPException(500, str(e))

@app.post("/clean/items")
def post_items(payload: List[Dict[str, Any]]):
    try: return tratar_itens_pedidos(payload)
    except Exception as e: raise HTTPException(500, str(e))