"""Grava a golden master: roda cada caso no código ORIGINAL e salva as saídas.

Uso (na raiz do repositório, ANTES de refatorar):
  python -B exercicios/aula-2/golden_master/gerar.py --codigo caso
"""
import argparse
import json
import os
import sys

from casos import CASOS

PASTA = os.path.dirname(os.path.abspath(__file__))


def executar(caso, calcular_total):
    """Roda um caso com a flag NATAL no estado pedido."""
    os.environ["MINILOJA_PROMO_NATAL"] = "1" if caso.get("natal") else "0"
    return calcular_total(**caso["args"])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--codigo", default="caso", help="pasta que contém o pacote miniloja")
    p.add_argument("--saida", default=os.path.join(PASTA, "golden.json"))
    p.add_argument("--forcar", action="store_true", help="sobrescreve uma golden master existente")
    a = p.parse_args()

    if os.path.exists(a.saida) and not a.forcar:
        sys.exit(f"{a.saida} já existe. Use --forcar só se tiver certeza de que o código é o ORIGINAL.")

    sys.path.insert(0, os.path.abspath(a.codigo))
    from miniloja.calculo import calcular_total

    registros = [
        {"nome": c["nome"], "args": c["args"], "natal": c.get("natal", False),
         "saida": executar(c, calcular_total)}
        for c in CASOS
    ]

    with open(a.saida, "w", encoding="utf-8") as f:
        json.dump(registros, f, ensure_ascii=False, indent=2)
    print(f"Golden master gravada: {len(registros)} casos em {a.saida}")


if __name__ == "__main__":
    main()
