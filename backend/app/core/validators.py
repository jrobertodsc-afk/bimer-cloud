import re

def limpar_documento(doc: str) -> str:
    """Remove caracteres não numéricos de CPF/CNPJ."""
    return re.sub(r'[^0-9]', '', doc or '')

def validar_cpf(cpf: str) -> bool:
    """Valida CPF brasileiro com dígitos verificadores."""
    cpf = limpar_documento(cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for i in range(9, 11):
        soma = sum(int(cpf[j]) * ((i + 1) - j) for j in range(i))
        digito = (soma * 10 % 11) % 10
        if int(cpf[i]) != digito:
            return False
    return True

def validar_cnpj(cnpj: str) -> bool:
    """Valida CNPJ brasileiro com dígitos verificadores."""
    cnpj = limpar_documento(cnpj)
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma1 = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
    d1 = 0 if soma1 % 11 < 2 else 11 - (soma1 % 11)
    if int(cnpj[12]) != d1:
        return False
    soma2 = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
    d2 = 0 if soma2 % 11 < 2 else 11 - (soma2 % 11)
    return int(cnpj[13]) == d2

def validar_documento(doc: str) -> bool:
    """Valida CPF (11 dígitos) ou CNPJ (14 dígitos)."""
    limpo = limpar_documento(doc)
    if len(limpo) == 11:
        return validar_cpf(limpo)
    elif len(limpo) == 14:
        return validar_cnpj(limpo)
    return False

def formatar_cnpj(cnpj: str) -> str:
    """Formata CNPJ: XX.XXX.XXX/XXXX-XX"""
    cnpj = limpar_documento(cnpj)
    if len(cnpj) != 14:
        return cnpj
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

def formatar_cpf(cpf: str) -> str:
    """Formata CPF: XXX.XXX.XXX-XX"""
    cpf = limpar_documento(cpf)
    if len(cpf) != 11:
        return cpf
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
