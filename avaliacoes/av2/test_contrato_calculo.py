"""Testes de calcular_total derivados do contrato (caso/regras.md, R1), não do código.

Cada "esperado" foi calculado à mão a partir de R1, com arredondamento meio para cima (R1.5).
Os dois casos em que o código atual diverge do contrato ficam como expectedFailure (ver ADR-001
no registro da AV2): se alguém corrigir o código, viram "unexpected success" e a suíte fica vermelha,
avisando que o golden master e o ADR precisam ser revistos.

Uso, a partir da raiz do pacote:
  python -B avaliacoes/av2/test_contrato_calculo.py --codigo caso
"""
import argparse
import os
import sys
import unittest

p = argparse.ArgumentParser()
p.add_argument("--codigo", default="caso")
args, resto = p.parse_known_args()
sys.path.insert(0, os.path.abspath(args.codigo))

from miniloja.calculo import calcular_total  # noqa: E402


def item(preco, qtd=1):
    return [{"preco": preco, "qtd": qtd}]


class TestContratoCalculo(unittest.TestCase):
    # --- R1.1 / R1.3 / R1.4: frete e taxa por UF, sem cupom
    def test_pe_subtotal_multiplica_preco_por_quantidade(self):
        # 50,00 x 2 = 100,00; + 12,90 = 112,90; x 1,05 = 118,545 -> 118,55
        self.assertEqual(calcular_total(item(50.0, 2), None, "PE"), 118.55)

    def test_sp_frete_e_taxa(self):
        # 100,00 + 19,90 = 119,90; x 1,07 = 128,293 -> 128,29
        self.assertEqual(calcular_total(item(100.0), None, "SP"), 128.29)

    def test_rj_frete_e_taxa(self):
        # 40,00 + 21,50 = 61,50; x 1,06 = 65,19
        self.assertEqual(calcular_total(item(40.0), None, "RJ"), 65.19)

    def test_uf_desconhecida_usa_padrao(self):
        # 60,00 + 29,90 = 89,90; x 1,08 = 97,092 -> 97,09
        self.assertEqual(calcular_total(item(60.0), None, "XX"), 97.09)

    # --- R1.2: cupons
    def test_promo10(self):
        # 80,00 x 0,90 = 72,00; + 19,90 = 91,90; x 1,07 = 98,333 -> 98,33
        self.assertEqual(calcular_total(item(80.0), "PROMO10", "SP"), 98.33)

    def test_vip15(self):
        # 100,00 x 0,85 = 85,00; + 19,90 = 104,90; x 1,07 = 112,243 -> 112,24
        self.assertEqual(calcular_total(item(100.0), "VIP15", "SP"), 112.24)

    def test_natal_com_campanha_ativa(self):
        # 50,00 x 0,80 = 40,00; + 19,90 = 59,90; x 1,07 = 64,093 -> 64,09
        os.environ["MINILOJA_PROMO_NATAL"] = "1"
        try:
            self.assertEqual(calcular_total(item(50.0), "NATAL", "SP"), 64.09)
        finally:
            os.environ.pop("MINILOJA_PROMO_NATAL", None)

    def test_natal_sem_campanha_nao_desconta(self):
        # 50,00 + 19,90 = 69,90; x 1,07 = 74,793 -> 74,79
        os.environ.pop("MINILOJA_PROMO_NATAL", None)
        self.assertEqual(calcular_total(item(50.0), "NATAL", "SP"), 74.79)

    def test_fretegratis_zera_frete_e_nao_desconta(self):
        # 40,00 + 0,00 = 40,00; x 1,06 = 42,40
        self.assertEqual(calcular_total(item(40.0), "FRETEGRATIS", "RJ"), 42.40)

    def test_cupom_desconhecido_e_ignorado(self):
        # igual ao caso sem cupom em RJ: 65,19 (valor literal, não recalculado pelo código)
        self.assertEqual(calcular_total(item(40.0), "CUPOMFALSO", "RJ"), 65.19)

    # --- R1.3 / R1.6: frete grátis e ordem desconto -> frete -> taxa
    def test_acima_de_200_nao_paga_frete(self):
        # 250,00 >= 200,00 -> frete 0; x 1,05 = 262,50
        self.assertEqual(calcular_total(item(250.0), None, "PE"), 262.50)

    def test_desconto_vem_antes_do_frete(self):
        # 215,00 x 0,90 = 193,50 (< 200, paga frete); + 12,90 = 206,40; x 1,05 = 216,72
        self.assertEqual(calcular_total(item(215.0), "PROMO10", "PE"), 216.72)

    # --- Divergências registradas (ADR-001): o contrato vale, o código ainda não segue
    @unittest.expectedFailure
    def test_fronteira_exata_200_tem_frete_gratis(self):
        # R1.3 "maior ou igual": 100,00 x 2 = 200,00 -> frete 0; x 1,05 = 210,00 (código: 223,55)
        self.assertEqual(calcular_total(item(100.0, 2), None, "PE"), 210.00)

    @unittest.expectedFailure
    def test_arredondamento_meio_para_cima(self):
        # R1.5: 2,00 + 12,90 = 14,90; x 1,05 = 15,645 -> 15,65 (código: 15,64)
        self.assertEqual(calcular_total(item(2.0), None, "PE"), 15.65)


if __name__ == "__main__":
    r = unittest.main(argv=[sys.argv[0]] + resto, exit=False, verbosity=2).result
    sys.exit(0 if r.wasSuccessful() else 1)
