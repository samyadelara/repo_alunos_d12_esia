"""Cadastro de clientes."""
import re

_CLIENTES = []

_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _cpf_valido(cpf):
    """Dígitos verificadores válidos e não todos iguais; aceita pontuação."""
    digitos = re.sub(r"[.\-]", "", cpf)
    if not re.fullmatch(r"\d{11}", digitos) or len(set(digitos)) == 1:
        return False
    numeros = [int(d) for d in digitos]
    for tamanho in (9, 10):
        soma = sum(n * peso for n, peso in zip(numeros[:tamanho], range(tamanho + 1, 1, -1)))
        dv = (soma * 10) % 11 % 10
        if dv != numeros[tamanho]:
            return False
    return True


def _validar(payload):
    """Devolve a lista de todos os erros do payload (R3)."""
    erros = []
    for campo in ("nome", "email", "cpf"):
        valor = payload.get(campo)
        if not isinstance(valor, str) or not valor.strip():
            erros.append({"campo": campo, "erro": "campo obrigatório"})
        elif campo == "email" and not _EMAIL.match(valor):
            erros.append({"campo": "email", "erro": "formato inválido"})
        elif campo == "cpf" and not _cpf_valido(valor):
            erros.append({"campo": "cpf", "erro": "cpf inválido"})
    return erros


def cadastrar_cliente(payload):
    """Cadastra um cliente; inválido responde 422 com todos os erros."""
    erros = _validar(payload)
    if erros:
        return 422, {"erros": erros}
    cliente = dict(payload, id=len(_CLIENTES) + 1)
    _CLIENTES.append(cliente)
    return 201, cliente


def limpar():
    _CLIENTES.clear()
