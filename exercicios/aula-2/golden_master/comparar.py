"""Compara o código atual com a golden master, por igualdade exata (sem tolerância).

Uso (na raiz do repositório, DEPOIS de refatorar):
  python -B exercicios/aula-2/golden_master/comparar.py --codigo caso

Código de saída: 0 = tudo igual; 1 = alguma saída mudou.
"""
import argparse
import json
import os
import sys

PASTA = os.path.dirname(os.path.abspath(__file__))


def identico(esperado, atual):
    """Igualdade exata, sem tolerância: mesmo tipo e mesma representação.

    Mais estrito que ==, que aceitaria 105 == 105.0 e 0.0 == -0.0.
    repr de float é exato (reconstrói o mesmo número bit a bit).
    """
    return type(esperado) is type(atual) and repr(esperado) == repr(atual)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--codigo", default="caso", help="pasta que contém o pacote miniloja")
    p.add_argument("--golden", default=os.path.join(PASTA, "golden.json"))
    a = p.parse_args()

    with open(a.golden, encoding="utf-8") as f:
        registros = json.load(f)

    sys.path.insert(0, os.path.abspath(a.codigo))
    from miniloja.calculo import calcular_total

    divergencias = 0
    for r in registros:
        os.environ["MINILOJA_PROMO_NATAL"] = "1" if r["natal"] else "0"
        try:
            atual = calcular_total(**r["args"])
        except Exception as e:  # uma exceção nova também é mudança de comportamento
            atual = f"ERRO: {type(e).__name__}: {e}"
        if not identico(r["saida"], atual):
            divergencias += 1
            print(f"DIFERENTE  {r['nome']}: esperado {r['saida']!r}, obtido {atual!r}")

    total = len(registros)
    print(f"\n{total - divergencias}/{total} casos iguais; {divergencias} diferente(s).")
    sys.exit(1 if divergencias else 0)


if __name__ == "__main__":
    main()
