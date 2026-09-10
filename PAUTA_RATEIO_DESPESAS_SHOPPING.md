# 📌 Pauta Técnica: Rateio Contábil & Desmembramento de Boletos de Shopping / Ocupação

**Projeto**: Bimer Cloud ERP — JR Solutions  
**Data de Registro**: 10/09/2026  
**Solicitante**: Roberto  
**Status**: Anotado para Desenvolvimento Futuro  

---

## 🏢 1. O Problema / Cenário Real
No varejo físico (especialmente em lojas de shopping como **Shopping da Bahia**, **Salvador Shopping**, **Shopping Barra**, **Paseo Itaigara**, **Parque Shopping Vilas**):
* O shopping emite **um único boleto bancário** com valor total consolidado (ex: R$ 18.450,00).
* Porém, dentro do boleto / espelho de cobrança mensal, há o **desmembramento (reparto) de múltiplos custos distintos**:
  1. **Aluguel Mínimo / Percentual** (Custo de Ocupação da Loja)
  2. **Condomínio Geral / Ordinário** (Manutenção, Limpeza, Segurança do Shopping)
  3. **Fundo de Promoção e Propaganda - FPP** (Marketing e Eventos do Shopping)
  4. **IPTU Fracionado da Loja** (Tributo Municipal)
  5. **Energia Elétrica (Submedição)** (Consumo de Luz da Loja)
  6. **Ar Condicionado Central / Chilled Water** (Refrigeração da Loja)
  7. **Água / Esgoto / Gás** (Consumo de Utilidades)
  8. **Taxa de Administração**

---

## ⚖️ 2. Regra Contábil & Financeira (Padrão Bimer / Alterdata)

### A) Visão Financeira (Contas a Pagar & Conciliação Bancária):
* O pagamento é **único**: 1 único código de barras / linha digitável Febraban, 1 único débito de extrato no Banco Itaú.
* Se fossem gerados 6 títulos separados, o financeiro não conseguiria pagar o boleto nem conciliar com o extrato bancário sem dar divergência de centavos ou de código de barras.
* **Solução Técnica**: Manter **1 único título financeiro** no valor cheio para quitação e conciliação bancária.

### B) Visão Contábil & Gerencial (DRE & Centro de Custo por Loja):
* Na apuração gerencial (Aba 7 / Relatório C por Centro de Custo da Loja SDB), cada despesa precisa cair na sua conta contábil correta:
  * O IPTU entra em *Impostos & Taxas*;
  * A Energia e o Ar Condicionado entram em *Utilidades & Consumo Operacional*;
  * O Aluguel entra em *Despesas de Ocupação*;
  * O FPP entra em *Marketing & Vendas*.
* **Solução Técnica**: Tabela filha `nota_rateios` vinculada à nota principal, onde o operador informa os itens do boleto.

---

## 🛠️ 3. Especificação da Solução a Ser Implementada

### No Frontend (Aba 1):
* Adicionar um bloco dobrável (acordeão): **`➕ Rateio Contábil de Despesas (Shopping / Condomínio)`**.
* Grade dinâmica com colunas:
  * **Conta Gerencial / Rubrica**: `[Aluguel | Condomínio | IPTU | Energia | Ar Condicionado | FPP | Outros]`
  * **Centro de Custo**: Loja Shopping da Bahia (ou filial específica)
  * **Valor do Item (R$)**: Ex: R$ 7.200,00
  * **% do Boleto**: Calculado automaticamente
* Validador em tempo real: a soma dos itens do rateio deve bater exatamente com o **Valor Bruto do Boleto** (trava contra erros de digitação).

### Na Folha de Rosto:
* Exibir um quadro analítico: **"Demonstrativo de Rateio Interno do Documento"**, detalhando quanto do boleto do Shopping da Bahia foi para Aluguel, IPTU, Energia e Condomínio.

### No Banco de Dados:
* Tabela `nota_rateios`:
  * `id INTEGER PRIMARY KEY`
  * `nota_id INTEGER`
  * `rubrica TEXT` (ex: "ENERGIA_ELETRICA", "IPTU", "AR_CONDICIONADO", "ALUGUEL", "CONDOMINIO", "FPP")
  * `centro_custo TEXT`
  * `valor REAL`
  * `percentual REAL`

---

## 📅 Próximo Passo
Essa pauta está anotada e mapeada com todas as diretrizes contábeis e fiscais para execução posterior.
