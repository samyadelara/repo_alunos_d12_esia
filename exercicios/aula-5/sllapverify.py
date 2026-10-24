import sys, csv; sys.path.insert(0, "caso")
from miniloja import handlers
handlers.post_pedidos(1, {"itens": [{"sku": "BOLA-01", "preco": 50.0, "qtd": 1}]})
handlers.post_pedidos(2, {"itens": [{"sku": "BOLA-01", "preco": 80.0, "qtd": 1}]})
# print(handlers.get_exportacao(1, "r4.csv"))
# print(open("exports/r4.csv", encoding="utf-8").read())   # aparecem pedidos do usuário 2?

# print(handlers.get_exportacao(1, "../fora_da_pasta.csv"))
print(handlers.get_exportacao(1, "pasta_inexistente/x.csv"))