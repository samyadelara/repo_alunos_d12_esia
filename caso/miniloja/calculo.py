"""Cálculo de totais de pedido."""
from miniloja import flags

FRETE_POR_UF = {"PE": 12.9, "SP": 19.9, "RJ": 21.5}
TAXA_POR_UF = {"PE": 0.05, "SP": 0.07, "RJ": 0.06}


FRETE_OUTRAS_UFS = 29.9
TAXA_OUTRAS_UFS = 0.08
LIMITE_FRETE_GRATIS = 200
FATOR_DESCONTO = {"PROMO10": 0.9, "VIP15": 0.85}


def _subtotal(itens):
    return sum(item["preco"] * item["qtd"] for item in itens)


def _fator_desconto(cupom):
    """Fator multiplicativo do cupom, ou None se o cupom não dá desconto."""
    if cupom == "NATAL":
        return 0.8 if flags.promo_natal_ativa() else None
    return FATOR_DESCONTO.get(cupom)


def _frete(valor, cupom, uf):
    if cupom == "FRETEGRATIS" or valor > LIMITE_FRETE_GRATIS:
        return 0
    return FRETE_POR_UF.get(uf, FRETE_OUTRAS_UFS)


def calcular_total(itens, cupom=None, uf="PE"):
    """Calcula o total do pedido: subtotal, desconto, frete e taxa de serviço."""
    total = _subtotal(itens)

    fator = _fator_desconto(cupom)
    if fator is not None:
        total = total * fator

    total = total + _frete(total, cupom, uf)
    total = total + total * TAXA_POR_UF.get(uf, TAXA_OUTRAS_UFS)

    return round(total, 2)
