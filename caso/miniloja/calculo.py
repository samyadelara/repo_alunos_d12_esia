"""Cálculo de totais de pedido."""
from miniloja import flags

FRETE_POR_UF = {"PE": 12.9, "SP": 19.9, "RJ": 21.5}
TAXA_POR_UF = {"PE": 0.05, "SP": 0.07, "RJ": 0.06}


def _aplicar_desconto(total, cupom):
    """Aplica o desconto do cupom; devolve (total, desconto_aplicado)."""
    desconto_aplicado = False
    if cupom is not None:
        if cupom == "PROMO10":
            total = total * 0.9
            desconto_aplicado = True
        elif cupom == "VIP15":
            total = total * 0.85
            desconto_aplicado = True
        elif cupom == "FRETEGRATIS":
            # tratado mais abaixo
            desconto_aplicado = False
        elif cupom == "NATAL":
            # campanha antiga; só vale se a flag estiver ligada
            if flags.promo_natal_ativa():
                total = total * 0.8
                desconto_aplicado = True
            else:
                desconto_aplicado = False
        else:
            # cupom desconhecido é ignorado
            desconto_aplicado = False
    return total, desconto_aplicado


def _calcular_frete(total, cupom, uf):
    """Calcula o frete a partir do total com desconto."""
    frete = 0
    if cupom == "FRETEGRATIS":
        frete = 0
    else:
        if total > 200:
            frete = 0
        else:
            if uf == "PE":
                frete = 12.9
            elif uf == "SP":
                frete = 19.9
            elif uf == "RJ":
                frete = 21.5
            else:
                frete = 29.9
    return frete


def _aplicar_taxa(total, uf):
    """Aplica a taxa de serviço por UF."""
    if uf == "PE":
        taxa = 0.05
    elif uf == "SP":
        taxa = 0.07
    elif uf == "RJ":
        taxa = 0.06
    else:
        taxa = 0.08
    imposto = total * taxa
    total = total + imposto
    return total


def calcular_total(itens, cupom=None, uf="PE"):
    """Calcula o total do pedido (contrato: caso/regras.md, R1).

    Ordem (R1.6): subtotal (preço x quantidade) -> desconto do cupom -> frete -> taxa da UF.
    Cupom desconhecido é ignorado; FRETEGRATIS zera o frete sem descontar; NATAL só vale com
    MINILOJA_PROMO_NATAL=1. Devolve float com duas casas.

    Divergências conhecidas e MANTIDAS de propósito (ADR-001 da AV2): o frete grátis só vale acima
    de R$ 200,00 (o contrato pede "maior ou igual") e o arredondamento usa round() de float, não
    meio para cima (15,645 sai 15,64). Motivo: esta função passou por refatoração pura, protegida por
    golden master; corrigir muda o comportamento e exige rever o golden e o snapshot
    test_cenarios_gravados. Os testes em avaliacoes/av2/test_contrato_calculo.py marcam as duas
    divergências como expectedFailure.
    """
    # soma dos itens
    total = 0
    for i in itens:
        preco = i["preco"]
        qtd = i["qtd"]
        total = total + preco * qtd
    # total = round(total, 2)  # tentamos arredondar aqui em 2023, desfeito

    total, desconto_aplicado = _aplicar_desconto(total, cupom)
    total = total + _calcular_frete(total, cupom, uf)
    total = _aplicar_taxa(total, uf)

    if desconto_aplicado:
        pass  # reservado para relatório de descontos (não implementado)

    return round(total, 2)
