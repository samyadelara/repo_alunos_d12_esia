"""Entradas da golden master de calcular_total, por classe de equivalência e limites (R1).

Só entradas possíveis pelo contrato: carrinho com itens (R2 rejeita pedido vazio).

Cada caso tem:
  nome  -> classe e descrição (aparece no relatório)
  args  -> argumentos passados para calcular_total
  natal -> True liga a campanha MINILOJA_PROMO_NATAL; False desliga (padrão)
"""

CEM = [{"preco": 100, "qtd": 1}]  # subtotal 100.00, abaixo do limite de frete


def item(preco, qtd=1):
    return [{"preco": preco, "qtd": qtd}]


CASOS = [
    # Classe cupom (7 classes), subtotal 100 em PE
    {"nome": "cupom: sem cupom", "args": {"itens": CEM, "cupom": None, "uf": "PE"}},
    {"nome": "cupom: PROMO10", "args": {"itens": CEM, "cupom": "PROMO10", "uf": "PE"}},
    {"nome": "cupom: VIP15", "args": {"itens": CEM, "cupom": "VIP15", "uf": "PE"}},
    {"nome": "cupom: FRETEGRATIS", "args": {"itens": CEM, "cupom": "FRETEGRATIS", "uf": "PE"}},
    {"nome": "cupom: NATAL campanha ativa", "args": {"itens": CEM, "cupom": "NATAL", "uf": "PE"}, "natal": True},
    {"nome": "cupom: NATAL campanha inativa", "args": {"itens": CEM, "cupom": "NATAL", "uf": "PE"}},
    {"nome": "cupom: desconhecido", "args": {"itens": CEM, "cupom": "XYZ", "uf": "PE"}},

    # Classe UF (4 classes), subtotal 100 sem cupom
    {"nome": "UF: SP", "args": {"itens": CEM, "cupom": None, "uf": "SP"}},
    {"nome": "UF: RJ", "args": {"itens": CEM, "cupom": None, "uf": "RJ"}},
    {"nome": "UF: demais (BA)", "args": {"itens": CEM, "cupom": None, "uf": "BA"}},

    # Cupom x UF: cada cupom também fora de PE
    {"nome": "cupom x UF: PROMO10, SP", "args": {"itens": CEM, "cupom": "PROMO10", "uf": "SP"}},
    {"nome": "cupom x UF: VIP15, RJ", "args": {"itens": CEM, "cupom": "VIP15", "uf": "RJ"}},
    {"nome": "cupom x UF: FRETEGRATIS, demais (BA)", "args": {"itens": CEM, "cupom": "FRETEGRATIS", "uf": "BA"}},
    {"nome": "cupom x UF: NATAL ativa, SP", "args": {"itens": CEM, "cupom": "NATAL", "uf": "SP"}, "natal": True},
    {"nome": "cupom x UF: desconhecido, RJ", "args": {"itens": CEM, "cupom": "XYZ", "uf": "RJ"}},

    # Limite do frete grátis: subtotal com desconto em 199.99 / 200.00 / 200.01
    {"nome": "limite frete: 199.99, PE", "args": {"itens": item(199.99), "cupom": None, "uf": "PE"}},
    {"nome": "limite frete: 200.00, PE", "args": {"itens": item(50, 4), "cupom": None, "uf": "PE"}},
    {"nome": "limite frete: 200.01, PE", "args": {"itens": item(200.01), "cupom": None, "uf": "PE"}},
    {"nome": "limite frete: 200.00, demais (BA)", "args": {"itens": item(200), "cupom": None, "uf": "BA"}},

    # Limite do frete com desconto aplicado antes (ordem: desconto, frete, taxa)
    {"nome": "desconto x frete: 220 com PROMO10 = 198, PE", "args": {"itens": item(110, 2), "cupom": "PROMO10", "uf": "PE"}},
    {"nome": "desconto x frete: 240 com VIP15 = 204, RJ", "args": {"itens": item(120, 2), "cupom": "VIP15", "uf": "RJ"}},
    {"nome": "desconto x frete: 250 com NATAL ativa = 200, SP", "args": {"itens": item(250), "cupom": "NATAL", "uf": "SP"}, "natal": True},
    {"nome": "desconto x frete: 250 com NATAL inativa, SP", "args": {"itens": item(250), "cupom": "NATAL", "uf": "SP"}},
    {"nome": "desconto x frete: FRETEGRATIS acima de 200, demais (BA)", "args": {"itens": item(225.5), "cupom": "FRETEGRATIS", "uf": "BA"}},

    # Subtotal: vários itens e quantidade > 1
    {"nome": "subtotal: vários itens, SP", "args": {"itens": [{"preco": 150, "qtd": 1}, {"preco": 25.5, "qtd": 2}], "cupom": None, "uf": "SP"}},
    {"nome": "subtotal: quantidade 3 com centavos, PE", "args": {"itens": item(19.99, 3), "cupom": None, "uf": "PE"}},
    {"nome": "subtotal: centavos com VIP15, RJ", "args": {"itens": item(19.99, 3), "cupom": "VIP15", "uf": "RJ"}},

    # Arredondamento: valor exato termina em meio centavo (R1.5: meio para cima)
    {"nome": "arredondamento: 24.045 exato, PE", "args": {"itens": item(10.0), "cupom": None, "uf": "PE"}},
    {"nome": "arredondamento: 24.255 exato, PE", "args": {"itens": item(10.2), "cupom": None, "uf": "PE"}},
]
