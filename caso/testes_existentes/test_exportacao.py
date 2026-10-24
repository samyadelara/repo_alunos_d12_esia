import unittest
from unittest.mock import patch

from miniloja import handlers
from miniloja.exportacao import exportar_vendas


class TestExportacao(unittest.TestCase):
    def test_exportar_vendas(self):
        with patch.object(handlers, "_repo") as repo:
            repo.todos.return_value = [
                {"id": 1, "usuario_id": 1, "total": 10.0},
                {"id": 2, "usuario_id": 2, "total": 20.0},
            ]
            status, corpo = exportar_vendas(1, "vendas.csv")
        self.assertEqual(status, 200)
        self.assertEqual(corpo["linhas"], 2)
