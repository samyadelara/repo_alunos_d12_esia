"""Cadastro de clientes."""

_CLIENTES = []


def _digito_verificador(digitos):
    """Calcula um dígito verificador do CPF (pesos decrescentes até 2)."""
    peso_inicial = len(digitos) + 1
    soma = sum(int(d) * (peso_inicial - i) for i, d in enumerate(digitos))
    resto = soma % 11
    return "0" if resto < 2 else str(11 - resto)


def cpf_valido(cpf):
    """R3.2: dígitos verificadores válidos, sem todos os dígitos iguais; aceita pontuação."""
    if not isinstance(cpf, str):
        return False
    digitos = cpf.replace(".", "").replace("-", "")
    if len(digitos) != 11 or not digitos.isdigit():
        return False
    if len(set(digitos)) == 1:
        return False
    dv1 = _digito_verificador(digitos[:9])
    dv2 = _digito_verificador(digitos[:9] + dv1)
    return digitos[9:] == dv1 + dv2


def cadastrar_cliente(payload):
    """Cadastra um cliente."""
    if not payload.get("nome"):
        return 400, {"erro": "payload inválido"}
    if not payload.get("email"):
        return 400, {"erro": "payload inválido"}
    if "cpf" in payload and not cpf_valido(payload["cpf"]):
        return 422, {"erros": [{"campo": "cpf", "erro": "cpf inválido"}]}
    cliente = dict(payload, id=len(_CLIENTES) + 1)
    _CLIENTES.append(cliente)
    return 201, cliente


def limpar():
    _CLIENTES.clear()
