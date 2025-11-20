from app.services.data_cleaning import tratar_itens_pedidos

# Nome do arquivo original (Renomeie o seu arquivo da Júlia para este nome!)
arquivo_entrada = "itens_pedidos.csv"
arquivo_saida = "itens_pedidos_tratados.csv"

try:
    # Chama a função que criamos acima
    df_limpo = tratar_itens_pedidos(arquivo_entrada)
    
    # Salva o resultado para você ver
    df_limpo.to_csv(arquivo_saida, index=False)
    
    print(f"✅ Sucesso! Arquivo gerado: {arquivo_saida}")
    print("Abra o arquivo e confira se 'price' está com ponto e sem buracos.")
    
except FileNotFoundError:
    print(f"❌ Erro: Não achei o arquivo '{arquivo_entrada}'. Renomeie o arquivo da Júlia!")