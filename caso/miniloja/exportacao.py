"""Exportação de vendas em CSV."""
import csv
import os

from miniloja import handlers

EXPORT_DIR = "exports"


def _br(v):
    return "R$ " + "{:,.2f}".format(v).replace(",", "X").replace(".", ",").replace("X", ".")


def exportar_vendas(usuario_id, nome_arquivo):
    pedidos = handlers._repo.todos()
    os.makedirs(EXPORT_DIR, exist_ok=True)
    caminho = os.path.join(EXPORT_DIR, nome_arquivo)
    try:
        with open(caminho, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["id", "usuario_id", "total"])
            for p in pedidos:
                w.writerow([p["id"], p["usuario_id"], _br(p["total"])])
    except Exception:
        pass
    return 200, {"arquivo": caminho, "linhas": len(pedidos)}
