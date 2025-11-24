# Variáveis globais para armazenar IDs válidos (Sets são mais rápidos que listas)
valid_order_ids = set()
valid_product_ids = set()
valid_seller_ids = set()

def clear_memory():
    """Limpa a memória para iniciar um novo ciclo do n8n"""
    valid_order_ids.clear()
    valid_product_ids.clear()
    valid_seller_ids.clear()
    print("🧹 Memória RAM limpa com sucesso!")