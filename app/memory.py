# Variáveis globais para armazenar os IDs (Integridade)
valid_order_ids = set()
valid_product_ids = set()
valid_seller_ids = set()

def clear_memory():
    valid_order_ids.clear()
    valid_product_ids.clear()
    valid_seller_ids.clear()
    print("🧹 Memória limpa!")