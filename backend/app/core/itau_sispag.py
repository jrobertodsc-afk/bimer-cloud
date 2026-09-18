"""
Gerador de Arquivo de Remessa CNAB 240 / SISPAG Itaú
Permite o agendamento em lote de boletos, tributos e PIX no Itaú Empresas.
Layout Padrão Febraban / Itaú SISPAG (240 posições por linha).
"""

import re
from datetime import datetime

def linha_digitavel_para_codigo_barras(linha):
    """
    Converte linha digitável de boleto bancário (47 dígitos) para código de barras (44 dígitos).
    Formato da linha: AAABC.CCCCX DDDDD.DDDDDY EEEEE.EEEEEZ K UUUUVVVVVVVVVV
    Formato de barras: AAABKUUUUVVVVVVVVVVCCCCCDDDDDDDDDDEEEEEEEEEE
    """
    if not linha:
        return ""
    limpa = re.sub(r"\D", "", str(linha))
    if len(limpa) == 47:
        banco_moeda = limpa[0:4]       # AAAB
        dv_geral = limpa[32:33]          # K
        fator_valor = limpa[33:47]       # UUUUVVVVVVVVVV
        campo1 = limpa[4:9]             # CCCCC
        campo2 = limpa[10:20]           # DDDDDDDDDD
        campo3 = limpa[21:31]           # EEEEEEEEEE
        return f"{banco_moeda}{dv_geral}{fator_valor}{campo1}{campo2}{campo3}"
    elif len(limpa) == 48:
        # Concessionária / Arrecadação (4 blocos de 12 dígitos, retira o 12º dígito de cada bloco)
        return limpa[0:11] + limpa[12:23] + limpa[24:35] + limpa[36:47]
    elif len(limpa) == 44:
        return limpa
    return ""

def formatar_campo(texto, tamanho, tipo="X"):
    """
    Formata campo para o CNAB:
    tipo="X": Alfa (preenchido com espaços à direita)
    tipo="9": Numérico (preenchido com zeros à esquerda)
    """
    if texto is None:
        texto = ""
    texto_str = str(texto)
    if tipo == "9":
        texto_limpo = re.sub(r"\D", "", texto_str)
        return texto_limpo.zfill(tamanho)[:tamanho]
    else:
        import unicodedata
        nfkd = unicodedata.normalize('NFKD', texto_str)
        sem_acento = "".join([c for c in nfkd if not unicodedata.combining(c)])
        return sem_acento.ljust(tamanho)[:tamanho]

def gerar_cnab240_sispag_itau(titulos, cnpj_empresa="10436619000288", razao_social="BOAH MODAS LTDA", agencia="0000", conta="00000", dac="0", data_pagamento=None):
    """
    Gera as linhas do arquivo CNAB 240 / SISPAG para pagamento de fornecedores (Itaú).
    """
    linhas = []
    hoje = datetime.now()
    data_geracao = hoje.strftime("%d%m%Y")
    hora_geracao = hoje.strftime("%H%M%S")
    
    if not data_pagamento:
        dt_pgto_str = data_geracao
    elif "-" in data_pagamento:
        dt_obj = datetime.strptime(data_pagamento, "%Y-%m-%d")
        dt_pgto_str = dt_obj.strftime("%d%m%Y")
    elif "/" in data_pagamento:
        parts = data_pagamento.split("/")
        dt_pgto_str = f"{parts[0].zfill(2)}{parts[1].zfill(2)}{parts[2]}"
    else:
        dt_pgto_str = str(data_pagamento)

    # 1. HEADER DE ARQUIVO (Registro 0)
    h_banco = "341"
    h_lote = "0000"
    h_tipo = "0"
    h_brancos1 = " " * 9
    h_tipo_insc = "2" # CNPJ
    h_num_insc = formatar_campo(cnpj_empresa, 14, "9")
    h_convenio = formatar_campo("", 20, "X")
    h_agencia = formatar_campo(agencia, 5, "9")
    h_branco_ag = " "
    h_conta = formatar_campo(conta, 12, "9")
    h_dac = formatar_campo(dac, 1, "X")
    h_branco_dac = " "
    h_nome_emp = formatar_campo(razao_social, 30, "X")
    h_nome_banco = formatar_campo("BANCO ITAU SA", 30, "X")
    h_brancos2 = " " * 10
    h_cod_rem = "1"
    h_dt_ger = data_geracao
    h_hr_ger = hora_geracao
    h_zeros = "0" * 9
    h_densidade = "00000"
    h_reservado = " " * 69
    
    linha_header_arq = (
        h_banco + h_lote + h_tipo + h_brancos1 + h_tipo_insc + h_num_insc +
        h_convenio + h_agencia + h_branco_ag + h_conta + h_dac + h_branco_dac +
        h_nome_emp + h_nome_banco + h_brancos2 + h_cod_rem + h_dt_ger + h_hr_ger +
        h_zeros + h_densidade + h_reservado
    )
    linhas.append(linha_header_arq[:240])

    # 2. HEADER DE LOTE (Registro 1) - Pagamento Fornecedores
    hl_banco = "341"
    hl_lote = "0001"
    hl_tipo = "1"
    hl_operacao = "C" # Crédito
    hl_servico = "20" # Pagamento Fornecedores
    hl_forma_pgto = "30" # Títulos
    hl_layout_lote = "040"
    hl_branco1 = " "
    hl_tipo_insc = "2"
    hl_num_insc = formatar_campo(cnpj_empresa, 14, "9")
    hl_convenio = formatar_campo("", 20, "X")
    hl_agencia = formatar_campo(agencia, 5, "9")
    hl_branco_ag = " "
    hl_conta = formatar_campo(conta, 12, "9")
    hl_dac = formatar_campo(dac, 1, "X")
    hl_branco_dac = " "
    hl_nome_emp = formatar_campo(razao_social, 30, "X")
    hl_info1 = formatar_campo("", 40, "X")
    hl_logradouro = formatar_campo("", 30, "X")
    hl_numero = formatar_campo("0", 5, "9")
    hl_compl = formatar_campo("", 15, "X")
    hl_cidade = formatar_campo("SALVADOR", 20, "X")
    hl_cep = formatar_campo("40000000", 8, "9")
    hl_uf = "BA"
    hl_brancos2 = " " * 18

    linha_header_lote = (
        hl_banco + hl_lote + hl_tipo + hl_operacao + hl_servico + hl_forma_pgto +
        hl_layout_lote + hl_branco1 + hl_tipo_insc + hl_num_insc + hl_convenio +
        hl_agencia + hl_branco_ag + hl_conta + hl_dac + hl_branco_dac +
        hl_nome_emp + hl_info1 + hl_logradouro + hl_numero + hl_compl +
        hl_cidade + hl_cep + hl_uf + hl_brancos2
    )
    linhas.append(linha_header_lote[:240])

    # 3. DETALHES (Segmento J para Boletos / Títulos)
    seq_registro = 0
    total_valor = 0.0

    for tit in titulos:
        seq_registro += 1
        valor_bruto = float(tit.get("valor_liquido") or tit.get("valor_bruto") or 0.0)
        total_valor += valor_bruto
        valor_centavos = int(round(valor_bruto * 100))
        
        linha_dig = tit.get("linha_dig") or tit.get("cod_barras") or ""
        codigo_barras = linha_digitavel_para_codigo_barras(linha_dig)
        
        venc = (tit.get("dt_vencimento") or "").replace("-", "").replace("/", "")
        if len(venc) == 8:
            if "/" in tit.get("dt_vencimento", ""):
                dt_venc_str = venc
            else:
                dt_venc_str = f"{venc[6:8]}{venc[4:6]}{venc[0:4]}"
        else:
            dt_venc_str = dt_pgto_str

        favorecido = tit.get("fornecedor") or "FORNECEDOR"
        num_doc = str(tit.get("numero_nf") or tit.get("numero_tx") or tit.get("id") or seq_registro)

        d_banco = "341"
        d_lote = "0001"
        d_tipo = "3"
        d_seq = str(seq_registro).zfill(5)
        d_seg = "J"
        d_tipo_mov = "0"
        d_cod_mov = "00"
        d_cod_barras = formatar_campo(codigo_barras, 44, "X")
        d_nome_fav = formatar_campo(favorecido, 30, "X")
        d_dt_venc = formatar_campo(dt_venc_str, 8, "9")
        d_val_nom = str(valor_centavos).zfill(15)
        d_val_desc = "0" * 15
        d_val_acresc = "0" * 15
        d_dt_pgto = dt_pgto_str
        d_val_pgto = str(valor_centavos).zfill(15)
        d_qtd_moeda = "0" * 15
        d_num_doc_emp = formatar_campo(num_doc, 20, "X")
        d_nosso_num = " " * 20
        d_cod_moeda = "09"
        d_brancos = " " * 16

        linha_detalhe = (
            d_banco + d_lote + d_tipo + d_seq + d_seg + d_tipo_mov + d_cod_mov +
            d_cod_barras + d_nome_fav + d_dt_venc + d_val_nom + d_val_desc +
            d_val_acresc + d_dt_pgto + d_val_pgto + d_qtd_moeda + d_num_doc_emp +
            d_nosso_num + d_cod_moeda + d_brancos
        )
        linhas.append(linha_detalhe[:240])

    # 4. TRAILLER DE LOTE (Registro 5)
    tl_banco = "341"
    tl_lote = "0001"
    tl_tipo = "5"
    tl_brancos1 = " " * 9
    total_registros_lote = seq_registro + 2
    tl_qtd_reg = str(total_registros_lote).zfill(6)
    total_centavos = int(round(total_valor * 100))
    tl_val_tot = str(total_centavos).zfill(18)
    tl_zeros1 = "0" * 18
    tl_brancos2 = " " * 181

    linha_trailler_lote = (
        tl_banco + tl_lote + tl_tipo + tl_brancos1 + tl_qtd_reg +
        tl_val_tot + tl_zeros1 + tl_brancos2
    )
    linhas.append(linha_trailler_lote[:240])

    # 5. TRAILLER DE ARQUIVO (Registro 9)
    ta_banco = "341"
    ta_lote = "9999"
    ta_tipo = "9"
    ta_brancos1 = " " * 9
    ta_qtd_lotes = "000001"
    total_registros_arquivo = len(linhas) + 1
    ta_qtd_reg = str(total_registros_arquivo).zfill(6)
    ta_zeros1 = "0" * 6
    ta_brancos2 = " " * 205

    linha_trailler_arquivo = (
        ta_banco + ta_lote + ta_tipo + ta_brancos1 + ta_qtd_lotes +
        ta_qtd_reg + ta_zeros1 + ta_brancos2
    )
    linhas.append(linha_trailler_arquivo[:240])

    return "\r\n".join(linhas) + "\r\n"
