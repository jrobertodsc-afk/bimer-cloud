// ==========================================================================
// PLANO DE CONTAS, GRUPOS E CATEGORIAS OFICIAIS (JR SOLUTIONS / BOAH)
// Origem: C:\Users\Roberto\Music\ARE DE T\Grupos e Categorias.xlsx
// ==========================================================================

const TABELA_GRUPOS_CATEGORIAS = [
  {
    "codigo": "11101",
    "nome": "Acervo Stilling",
    "rotulo": "11101 - Acervo Stilling",
    "macro": "1 - FIXOS",
    "grupo": "111 - Custo Fixo - Desenvolvimento de Produto (Estilo)",
    "responsavel": "Estilo"
  },
  {
    "codigo": "11102",
    "nome": "Estilista Terceiros (Salário)",
    "rotulo": "11102 - Estilista Terceiros (Salário)",
    "macro": "1 - FIXOS",
    "grupo": "111 - Custo Fixo - Desenvolvimento de Produto (Estilo)",
    "responsavel": "Estilo"
  },
  {
    "codigo": "11103",
    "nome": "Peças de Inspiração/ Pilotos (6 peças Mês)",
    "rotulo": "11103 - Peças de Inspiração/ Pilotos (6 peças Mês)",
    "macro": "1 - FIXOS",
    "grupo": "111 - Custo Fixo - Desenvolvimento de Produto (Estilo)",
    "responsavel": "Estilo"
  },
  {
    "codigo": "11104",
    "nome": "Peças Piloto de Terceiros",
    "rotulo": "11104 - Peças Piloto de Terceiros",
    "macro": "1 - FIXOS",
    "grupo": "111 - Custo Fixo - Desenvolvimento de Produto (Estilo)",
    "responsavel": "Estilo"
  },
  {
    "codigo": "11105",
    "nome": "Custos Com Viagens",
    "rotulo": "11105 - Custos Com Viagens",
    "macro": "1 - FIXOS",
    "grupo": "111 - Custo Fixo - Desenvolvimento de Produto (Estilo)",
    "responsavel": "Estilo"
  },
  {
    "codigo": "11201",
    "nome": "Produção - Cadista/Corte/Expedição/Modelagem/Pilotagem",
    "rotulo": "11201 - Produção - Cadista/Corte/Expedição/Modelagem/Pilotagem",
    "macro": "1 - FIXOS",
    "grupo": "112 - Custo Fixo - Produção Atelier",
    "responsavel": "Produção"
  },
  {
    "codigo": "21101",
    "nome": "Aluguel",
    "rotulo": "21101 - Aluguel",
    "macro": "1 - FIXOS",
    "grupo": "211 - Despesa Fixa - Administrativas",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21102",
    "nome": "Condominio",
    "rotulo": "21102 - Condominio",
    "macro": "1 - FIXOS",
    "grupo": "211 - Despesa Fixa - Administrativas",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21103",
    "nome": "Agua E Esgotos",
    "rotulo": "21103 - Agua E Esgotos",
    "macro": "1 - FIXOS",
    "grupo": "211 - Despesa Fixa - Administrativas",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21104",
    "nome": "Energia Eletrica",
    "rotulo": "21104 - Energia Eletrica",
    "macro": "1 - FIXOS",
    "grupo": "211 - Despesa Fixa - Administrativas",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21105",
    "nome": "Ar Condicionado",
    "rotulo": "21105 - Ar Condicionado",
    "macro": "1 - FIXOS",
    "grupo": "211 - Despesa Fixa - Administrativas",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21106",
    "nome": "Fundo De Promoção/Reserva",
    "rotulo": "21106 - Fundo De Promoção/Reserva",
    "macro": "1 - FIXOS",
    "grupo": "211 - Despesa Fixa - Administrativas",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21107",
    "nome": "Reembolso de Despesas Operacionais (Transporte, Alimentação Etc)",
    "rotulo": "21107 - Reembolso de Despesas Operacionais (Transporte, Alimentação Etc)",
    "macro": "1 - FIXOS",
    "grupo": "211 - Despesa Fixa - Administrativas",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21116",
    "nome": "Sindicato E Associações",
    "rotulo": "21116 - Sindicato E Associações",
    "macro": "1 - FIXOS",
    "grupo": "211 - Despesa Fixa - Administrativas",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21109",
    "nome": "Seguros Loja/Imóvel",
    "rotulo": "21109 - Seguros Loja/Imóvel",
    "macro": "1 - FIXOS",
    "grupo": "211 - Despesa Fixa - Administrativas",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21110",
    "nome": "Graficas Em Geral",
    "rotulo": "21110 - Graficas Em Geral",
    "macro": "1 - FIXOS",
    "grupo": "211 - Despesa Fixa - Administrativas",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21111",
    "nome": "Serviços Advocatícios",
    "rotulo": "21111 - Serviços Advocatícios",
    "macro": "1 - FIXOS",
    "grupo": "211 - Despesa Fixa - Administrativas",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21112",
    "nome": "Servicos Contabeis",
    "rotulo": "21112 - Servicos Contabeis",
    "macro": "1 - FIXOS",
    "grupo": "211 - Despesa Fixa - Administrativas",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21113",
    "nome": "Consultorias e Auditorias",
    "rotulo": "21113 - Consultorias e Auditorias",
    "macro": "1 - FIXOS",
    "grupo": "211 - Despesa Fixa - Administrativas",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21114",
    "nome": "Telefonia Fixa/Internet",
    "rotulo": "21114 - Telefonia Fixa/Internet",
    "macro": "1 - FIXOS",
    "grupo": "211 - Despesa Fixa - Administrativas",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21115",
    "nome": "Telefonia Movel",
    "rotulo": "21115 - Telefonia Movel",
    "macro": "1 - FIXOS",
    "grupo": "211 - Despesa Fixa - Administrativas",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21117",
    "nome": "Seguro Geral",
    "rotulo": "21117 - Seguro Geral",
    "macro": "1 - FIXOS",
    "grupo": "211 - Despesa Fixa - Administrativas",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21118",
    "nome": "Correios, Cartorios E Periodicos",
    "rotulo": "21118 - Correios, Cartorios E Periodicos",
    "macro": "1 - FIXOS",
    "grupo": "211 - Despesa Fixa - Administrativas",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21119",
    "nome": "Consulta Spc / Serasa",
    "rotulo": "21119 - Consulta Spc / Serasa",
    "macro": "1 - FIXOS",
    "grupo": "211 - Despesa Fixa - Administrativas",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21120",
    "nome": "Sistemas e Softwares",
    "rotulo": "21120 - Sistemas e Softwares",
    "macro": "1 - FIXOS",
    "grupo": "211 - Despesa Fixa - Administrativas",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21121",
    "nome": "Dominios, Emails E Site",
    "rotulo": "21121 - Dominios, Emails E Site",
    "macro": "1 - FIXOS",
    "grupo": "211 - Despesa Fixa - Administrativas",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21201",
    "nome": "Copa e Cozinha",
    "rotulo": "21201 - Copa e Cozinha",
    "macro": "1 - FIXOS",
    "grupo": "212 - Despesa Fixa - Operacional",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21202",
    "nome": "Dedetização",
    "rotulo": "21202 - Dedetização",
    "macro": "1 - FIXOS",
    "grupo": "212 - Despesa Fixa - Operacional",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21203",
    "nome": "Recarga de Extintores",
    "rotulo": "21203 - Recarga de Extintores",
    "macro": "1 - FIXOS",
    "grupo": "212 - Despesa Fixa - Operacional",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21204",
    "nome": "Material de Escritório",
    "rotulo": "21204 - Material de Escritório",
    "macro": "1 - FIXOS",
    "grupo": "212 - Despesa Fixa - Operacional",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21205",
    "nome": "Material de Informática (Recargas e Tonners",
    "rotulo": "21205 - Material de Informática (Recargas e Tonners",
    "macro": "1 - FIXOS",
    "grupo": "212 - Despesa Fixa - Operacional",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21206",
    "nome": "Material de Limpeza",
    "rotulo": "21206 - Material de Limpeza",
    "macro": "1 - FIXOS",
    "grupo": "212 - Despesa Fixa - Operacional",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21207",
    "nome": "Despesas com PET",
    "rotulo": "21207 - Despesas com PET",
    "macro": "1 - FIXOS",
    "grupo": "212 - Despesa Fixa - Operacional",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21208",
    "nome": "Prestações de Serviços Operacionais",
    "rotulo": "21208 - Prestações de Serviços Operacionais",
    "macro": "1 - FIXOS",
    "grupo": "212 - Despesa Fixa - Operacional",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21209",
    "nome": "Uso e Consumo Lojas (Copos, Comandas Etc)",
    "rotulo": "21209 - Uso e Consumo Lojas (Copos, Comandas Etc)",
    "macro": "1 - FIXOS",
    "grupo": "212 - Despesa Fixa - Operacional",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21301",
    "nome": "Combustíveis Motoboy",
    "rotulo": "21301 - Combustíveis Motoboy",
    "macro": "1 - FIXOS",
    "grupo": "213 - Despesa Fixa - Logística",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21302",
    "nome": "Estacionamento/Pedágio",
    "rotulo": "21302 - Estacionamento/Pedágio",
    "macro": "1 - FIXOS",
    "grupo": "213 - Despesa Fixa - Logística",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21303",
    "nome": "Licenciamento e Multas/IPVA Moto/Carro",
    "rotulo": "21303 - Licenciamento e Multas/IPVA Moto/Carro",
    "macro": "1 - FIXOS",
    "grupo": "213 - Despesa Fixa - Logística",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21304",
    "nome": "Manutenção - Moto/Carro",
    "rotulo": "21304 - Manutenção - Moto/Carro",
    "macro": "1 - FIXOS",
    "grupo": "213 - Despesa Fixa - Logística",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21305",
    "nome": "Seguros - Moto/Carro",
    "rotulo": "21305 - Seguros - Moto/Carro",
    "macro": "1 - FIXOS",
    "grupo": "213 - Despesa Fixa - Logística",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21306",
    "nome": "Táxi/Uber (200,00*3 por mês)",
    "rotulo": "21306 - Táxi/Uber (200,00*3 por mês)",
    "macro": "1 - FIXOS",
    "grupo": "213 - Despesa Fixa - Logística",
    "responsavel": "Planejamento / OPP"
  },
  {
    "codigo": "12201",
    "nome": "Salários",
    "rotulo": "12201 - Salários",
    "macro": "1 - FIXOS",
    "grupo": "214 - Despesa Fixa - Pessoal",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "12202",
    "nome": "Salários - Meis/PJ",
    "rotulo": "12202 - Salários - Meis/PJ",
    "macro": "1 - FIXOS",
    "grupo": "214 - Despesa Fixa - Pessoal",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "12203",
    "nome": "Prolabore",
    "rotulo": "12203 - Prolabore",
    "macro": "1 - FIXOS",
    "grupo": "214 - Despesa Fixa - Pessoal",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "12203",
    "nome": "Transportes",
    "rotulo": "12203 - Transportes",
    "macro": "1 - FIXOS",
    "grupo": "214 - Despesa Fixa - Pessoal",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "12204",
    "nome": "Alimentação",
    "rotulo": "12204 - Alimentação",
    "macro": "1 - FIXOS",
    "grupo": "214 - Despesa Fixa - Pessoal",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "12205",
    "nome": "FGTS",
    "rotulo": "12205 - FGTS",
    "macro": "1 - FIXOS",
    "grupo": "214 - Despesa Fixa - Pessoal",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "12205",
    "nome": "INSS",
    "rotulo": "12205 - INSS",
    "macro": "1 - FIXOS",
    "grupo": "214 - Despesa Fixa - Pessoal",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "12205",
    "nome": "IRRF - Imposto de Renda PF (Verificar %)",
    "rotulo": "12205 - IRRF - Imposto de Renda PF (Verificar %)",
    "macro": "1 - FIXOS",
    "grupo": "214 - Despesa Fixa - Pessoal",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "12206",
    "nome": "Férias",
    "rotulo": "12206 - Férias",
    "macro": "1 - FIXOS",
    "grupo": "214 - Despesa Fixa - Pessoal",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "12207",
    "nome": "Rescisão",
    "rotulo": "12207 - Rescisão",
    "macro": "1 - FIXOS",
    "grupo": "214 - Despesa Fixa - Pessoal",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "12207",
    "nome": "Muita de FGTS",
    "rotulo": "12207 - Muita de FGTS",
    "macro": "1 - FIXOS",
    "grupo": "214 - Despesa Fixa - Pessoal",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "12208",
    "nome": "Domingos e Feriados Trabalhados",
    "rotulo": "12208 - Domingos e Feriados Trabalhados",
    "macro": "1 - FIXOS",
    "grupo": "214 - Despesa Fixa - Pessoal",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "12208",
    "nome": "Cursos e Treinamentos",
    "rotulo": "12208 - Cursos e Treinamentos",
    "macro": "1 - FIXOS",
    "grupo": "214 - Despesa Fixa - Pessoal",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "12209",
    "nome": "Exames Clínicos (Dem/Adm/Per)",
    "rotulo": "12209 - Exames Clínicos (Dem/Adm/Per)",
    "macro": "1 - FIXOS",
    "grupo": "214 - Despesa Fixa - Pessoal",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "12210",
    "nome": "Despesas com Estágio",
    "rotulo": "12210 - Despesas com Estágio",
    "macro": "1 - FIXOS",
    "grupo": "214 - Despesa Fixa - Pessoal",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "12211",
    "nome": "13º salário",
    "rotulo": "12211 - 13º salário",
    "macro": "1 - FIXOS",
    "grupo": "214 - Despesa Fixa - Pessoal",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "12212",
    "nome": "Sindicatos",
    "rotulo": "12212 - Sindicatos",
    "macro": "1 - FIXOS",
    "grupo": "214 - Despesa Fixa - Pessoal",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "12213",
    "nome": "Extras",
    "rotulo": "12213 - Extras",
    "macro": "1 - FIXOS",
    "grupo": "214 - Despesa Fixa - Pessoal",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "12214",
    "nome": "Fardamento",
    "rotulo": "12214 - Fardamento",
    "macro": "1 - FIXOS",
    "grupo": "214 - Despesa Fixa - Pessoal",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "12215",
    "nome": "ISS Substituto Tributário",
    "rotulo": "12215 - ISS Substituto Tributário",
    "macro": "1 - FIXOS",
    "grupo": "214 - Despesa Fixa - Pessoal",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21501",
    "nome": "Manutenção - Predial",
    "rotulo": "21501 - Manutenção - Predial",
    "macro": "1 - FIXOS",
    "grupo": "215 - Despesa Fixa - Manutenção",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21502",
    "nome": "Manutenção - Elétrica",
    "rotulo": "21502 - Manutenção - Elétrica",
    "macro": "1 - FIXOS",
    "grupo": "215 - Despesa Fixa - Manutenção",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21503",
    "nome": "Manutenção - Informática",
    "rotulo": "21503 - Manutenção - Informática",
    "macro": "1 - FIXOS",
    "grupo": "215 - Despesa Fixa - Manutenção",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21504",
    "nome": "Manutenção - Maquinas e Equipamentos",
    "rotulo": "21504 - Manutenção - Maquinas e Equipamentos",
    "macro": "1 - FIXOS",
    "grupo": "215 - Despesa Fixa - Manutenção",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21505",
    "nome": "Manutenção - Refrigeração/Ar-condicionado",
    "rotulo": "21505 - Manutenção - Refrigeração/Ar-condicionado",
    "macro": "1 - FIXOS",
    "grupo": "215 - Despesa Fixa - Manutenção",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21506",
    "nome": "Manutenção - Mobiliário/Decoração",
    "rotulo": "21506 - Manutenção - Mobiliário/Decoração",
    "macro": "1 - FIXOS",
    "grupo": "215 - Despesa Fixa - Manutenção",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21601",
    "nome": "Tarifas Bancárias",
    "rotulo": "21601 - Tarifas Bancárias",
    "macro": "1 - FIXOS",
    "grupo": "216 - Despesa Fixa - Financeiras",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21602",
    "nome": "Aluguel de Maquinetas",
    "rotulo": "21602 - Aluguel de Maquinetas",
    "macro": "1 - FIXOS",
    "grupo": "216 - Despesa Fixa - Financeiras",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21603",
    "nome": "Taxa de Adm Cartões/Pix/Boletos",
    "rotulo": "21603 - Taxa de Adm Cartões/Pix/Boletos",
    "macro": "1 - FIXOS",
    "grupo": "216 - Despesa Fixa - Financeiras",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21701",
    "nome": "Comunicação/Mídia Digital - Despesas Operacionais/Fecebook/Email/Mailship/Agencia/Programas e apps",
    "rotulo": "21701 - Comunicação/Mídia Digital - Despesas Operacionais/Fecebook/Email/Mailship/Agencia/Programas e apps",
    "macro": "1 - FIXOS",
    "grupo": "217 - Despesa Fixa - Marketing",
    "responsavel": "Marketing"
  },
  {
    "codigo": "21705",
    "nome": "Relacionamento com o Cliente - Ações Clientes/Clube Boah/ Sistemas/Mimos",
    "rotulo": "21705 - Relacionamento com o Cliente - Ações Clientes/Clube Boah/ Sistemas/Mimos",
    "macro": "1 - FIXOS",
    "grupo": "217 - Despesa Fixa - Marketing",
    "responsavel": "Marketing"
  },
  {
    "codigo": "21704",
    "nome": "Marketing de Influencia - Blogueiras/Influencers/Eventos/Permutas)",
    "rotulo": "21704 - Marketing de Influencia - Blogueiras/Influencers/Eventos/Permutas)",
    "macro": "1 - FIXOS",
    "grupo": "217 - Despesa Fixa - Marketing",
    "responsavel": "Marketing"
  },
  {
    "codigo": "21703",
    "nome": "Lookbook (5 Por Ano)",
    "rotulo": "21703 - Lookbook (5 Por Ano)",
    "macro": "1 - FIXOS",
    "grupo": "217 - Despesa Fixa - Marketing",
    "responsavel": "Marketing"
  },
  {
    "codigo": "21702",
    "nome": "Editorial para Campanha (4 Por Ano)",
    "rotulo": "21702 - Editorial para Campanha (4 Por Ano)",
    "macro": "1 - FIXOS",
    "grupo": "217 - Despesa Fixa - Marketing",
    "responsavel": "Marketing"
  },
  {
    "codigo": "21706",
    "nome": "Visual Merchandising - Decoração Atelier/Acervo/Vitrines",
    "rotulo": "21706 - Visual Merchandising - Decoração Atelier/Acervo/Vitrines",
    "macro": "1 - FIXOS",
    "grupo": "217 - Despesa Fixa - Marketing",
    "responsavel": "Marketing"
  },
  {
    "codigo": "21707",
    "nome": "Material Gráfico",
    "rotulo": "21707 - Material Gráfico",
    "macro": "1 - FIXOS",
    "grupo": "217 - Despesa Fixa - Marketing",
    "responsavel": "Marketing"
  },
  {
    "codigo": "21801",
    "nome": "Endomarketing",
    "rotulo": "21801 - Endomarketing",
    "macro": "1 - FIXOS",
    "grupo": "218 - Despesa Fixa - Endomarketing",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21901",
    "nome": "IPTU",
    "rotulo": "21901 - IPTU",
    "macro": "1 - FIXOS",
    "grupo": "219 - Despesa Fixa - Tributos",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21902",
    "nome": "Taxas Municipais",
    "rotulo": "21902 - Taxas Municipais",
    "macro": "1 - FIXOS",
    "grupo": "219 - Despesa Fixa - Tributos",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "21903",
    "nome": "Taxas Estaduais",
    "rotulo": "21903 - Taxas Estaduais",
    "macro": "1 - FIXOS",
    "grupo": "219 - Despesa Fixa - Tributos",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "12101",
    "nome": "Tecidos",
    "rotulo": "12101 - Tecidos",
    "macro": "2 - VARIÁVEIS",
    "grupo": "121 - Custo Variável - Produção",
    "responsavel": "Compras"
  },
  {
    "codigo": "12102",
    "nome": "Aviamentos",
    "rotulo": "12102 - Aviamentos",
    "macro": "2 - VARIÁVEIS",
    "grupo": "121 - Custo Variável - Produção",
    "responsavel": "Compras"
  },
  {
    "codigo": "12103",
    "nome": "Insumos Gerais (produção)",
    "rotulo": "12103 - Insumos Gerais (produção)",
    "macro": "2 - VARIÁVEIS",
    "grupo": "121 - Custo Variável - Produção",
    "responsavel": "Compras"
  },
  {
    "codigo": "12104",
    "nome": "Produtos Para Revenda",
    "rotulo": "12104 - Produtos Para Revenda",
    "macro": "2 - VARIÁVEIS",
    "grupo": "121 - Custo Variável - Produção",
    "responsavel": "Compras"
  },
  {
    "codigo": "12105",
    "nome": "Embalagens",
    "rotulo": "12105 - Embalagens",
    "macro": "2 - VARIÁVEIS",
    "grupo": "121 - Custo Variável - Produção",
    "responsavel": "Compras"
  },
  {
    "codigo": "12106",
    "nome": "Sacolas",
    "rotulo": "12106 - Sacolas",
    "macro": "2 - VARIÁVEIS",
    "grupo": "121 - Custo Variável - Produção",
    "responsavel": "Compras"
  },
  {
    "codigo": "12107",
    "nome": "Etiquetas roupas/Acessorios",
    "rotulo": "12107 - Etiquetas roupas/Acessorios",
    "macro": "2 - VARIÁVEIS",
    "grupo": "121 - Custo Variável - Produção",
    "responsavel": "Compras"
  },
  {
    "codigo": "12108",
    "nome": "Lacres",
    "rotulo": "12108 - Lacres",
    "macro": "2 - VARIÁVEIS",
    "grupo": "121 - Custo Variável - Produção",
    "responsavel": "Compras"
  },
  {
    "codigo": "12109",
    "nome": "Prestação de Serviço - Corte",
    "rotulo": "12109 - Prestação de Serviço - Corte",
    "macro": "2 - VARIÁVEIS",
    "grupo": "121 - Custo Variável - Produção",
    "responsavel": "Compras"
  },
  {
    "codigo": "12110",
    "nome": "Faccionista - Conserto",
    "rotulo": "12110 - Faccionista - Conserto",
    "macro": "2 - VARIÁVEIS",
    "grupo": "121 - Custo Variável - Produção",
    "responsavel": "Compras"
  },
  {
    "codigo": "12111",
    "nome": "Faccionista - Mão de Obra",
    "rotulo": "12111 - Faccionista - Mão de Obra",
    "macro": "2 - VARIÁVEIS",
    "grupo": "121 - Custo Variável - Produção",
    "responsavel": "Compras"
  },
  {
    "codigo": "12112",
    "nome": "Frete/Transporte - Produção",
    "rotulo": "12112 - Frete/Transporte - Produção",
    "macro": "2 - VARIÁVEIS",
    "grupo": "121 - Custo Variável - Produção",
    "responsavel": "Compras"
  },
  {
    "codigo": "12113",
    "nome": "Faccionista - Confecção de Pilotos",
    "rotulo": "12113 - Faccionista - Confecção de Pilotos",
    "macro": "2 - VARIÁVEIS",
    "grupo": "121 - Custo Variável - Produção",
    "responsavel": "Compras"
  },
  {
    "codigo": "22101",
    "nome": "Bonificação / Premiação",
    "rotulo": "22101 - Bonificação / Premiação",
    "macro": "2 - VARIÁVEIS",
    "grupo": "221 - Despesa Variável - Pessoal",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "22102",
    "nome": "Comissões",
    "rotulo": "22102 - Comissões",
    "macro": "2 - VARIÁVEIS",
    "grupo": "221 - Despesa Variável - Pessoal",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "22201",
    "nome": "Entregas On-line",
    "rotulo": "22201 - Entregas On-line",
    "macro": "2 - VARIÁVEIS",
    "grupo": "222 - Despesa Variável - Com Vendas",
    "responsavel": "Online"
  },
  {
    "codigo": "22202",
    "nome": "Entregas Atacado",
    "rotulo": "22202 - Entregas Atacado",
    "macro": "2 - VARIÁVEIS",
    "grupo": "222 - Despesa Variável - Com Vendas",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "22203",
    "nome": "Plataforma de Vendas On-line",
    "rotulo": "22203 - Plataforma de Vendas On-line",
    "macro": "2 - VARIÁVEIS",
    "grupo": "222 - Despesa Variável - Com Vendas",
    "responsavel": "Online"
  },
  {
    "codigo": "22204",
    "nome": "Devolução de Vendas",
    "rotulo": "22204 - Devolução de Vendas",
    "macro": "2 - VARIÁVEIS",
    "grupo": "222 - Despesa Variável - Com Vendas",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "22205",
    "nome": "Aluguel Percentual",
    "rotulo": "22205 - Aluguel Percentual",
    "macro": "2 - VARIÁVEIS",
    "grupo": "222 - Despesa Variável - Com Vendas",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "22206",
    "nome": "Embalagens (Sacolas, Envelopes e Papel Seda)",
    "rotulo": "22206 - Embalagens (Sacolas, Envelopes e Papel Seda)",
    "macro": "2 - VARIÁVEIS",
    "grupo": "222 - Despesa Variável - Com Vendas",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "22207",
    "nome": "Ações Comerciais",
    "rotulo": "22207 - Ações Comerciais",
    "macro": "2 - VARIÁVEIS",
    "grupo": "222 - Despesa Variável - Com Vendas",
    "responsavel": "Planejamento / OPP"
  },
  {
    "codigo": "22601",
    "nome": "Juros Cheque Especial / IOF",
    "rotulo": "22601 - Juros Cheque Especial / IOF",
    "macro": "2 - VARIÁVEIS",
    "grupo": "226 - Despesa Variável - Financeira",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "22602",
    "nome": "Juros por Atraso de Pagamentos",
    "rotulo": "22602 - Juros por Atraso de Pagamentos",
    "macro": "2 - VARIÁVEIS",
    "grupo": "226 - Despesa Variável - Financeira",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "22701",
    "nome": "Contrato de Mutuo - Débito",
    "rotulo": "22701 - Contrato de Mutuo - Débito",
    "macro": "2 - VARIÁVEIS",
    "grupo": "227 - Despesa Variável - Contrato de Mutuo",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "22301",
    "nome": "ICMS",
    "rotulo": "22301 - ICMS",
    "macro": "3 - IMPOSTOS",
    "grupo": "223 - Despesa Variável - Impostos",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "22302",
    "nome": "ICMS Substituição Tributaria",
    "rotulo": "22302 - ICMS Substituição Tributaria",
    "macro": "3 - IMPOSTOS",
    "grupo": "223 - Despesa Variável - Impostos",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "22303",
    "nome": "ICMS Antecipação Parcial",
    "rotulo": "22303 - ICMS Antecipação Parcial",
    "macro": "3 - IMPOSTOS",
    "grupo": "223 - Despesa Variável - Impostos",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "22304",
    "nome": "PIS (8109)",
    "rotulo": "22304 - PIS (8109)",
    "macro": "3 - IMPOSTOS",
    "grupo": "223 - Despesa Variável - Impostos",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "22305",
    "nome": "COFINS (2172)",
    "rotulo": "22305 - COFINS (2172)",
    "macro": "3 - IMPOSTOS",
    "grupo": "223 - Despesa Variável - Impostos",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "22306",
    "nome": "IRPJ (2089)",
    "rotulo": "22306 - IRPJ (2089)",
    "macro": "3 - IMPOSTOS",
    "grupo": "223 - Despesa Variável - Impostos",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "22307",
    "nome": "CSLL (2372)",
    "rotulo": "22307 - CSLL (2372)",
    "macro": "3 - IMPOSTOS",
    "grupo": "223 - Despesa Variável - Impostos",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "22308",
    "nome": "Simples Nacional",
    "rotulo": "22308 - Simples Nacional",
    "macro": "3 - IMPOSTOS",
    "grupo": "223 - Despesa Variável - Impostos",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "22309",
    "nome": "GNRE",
    "rotulo": "22309 - GNRE",
    "macro": "3 - IMPOSTOS",
    "grupo": "223 - Despesa Variável - Impostos",
    "responsavel": "Financeiro / Administrativo"
  },
  {
    "codigo": "22401",
    "nome": "Investimento - Predial",
    "rotulo": "22401 - Investimento - Predial",
    "macro": "4 - INVESTIMENTOS",
    "grupo": "224 - Despesa Variável - Investimentos",
    "responsavel": "Diretoria"
  },
  {
    "codigo": "22402",
    "nome": "Investimento - Informática",
    "rotulo": "22402 - Investimento - Informática",
    "macro": "4 - INVESTIMENTOS",
    "grupo": "224 - Despesa Variável - Investimentos",
    "responsavel": "Diretoria"
  },
  {
    "codigo": "22403",
    "nome": "Investimento - Elétrica",
    "rotulo": "22403 - Investimento - Elétrica",
    "macro": "4 - INVESTIMENTOS",
    "grupo": "224 - Despesa Variável - Investimentos",
    "responsavel": "Diretoria"
  },
  {
    "codigo": "22404",
    "nome": "Investimento - Maquinas e Equipamentos",
    "rotulo": "22404 - Investimento - Maquinas e Equipamentos",
    "macro": "4 - INVESTIMENTOS",
    "grupo": "224 - Despesa Variável - Investimentos",
    "responsavel": "Diretoria"
  },
  {
    "codigo": "22405",
    "nome": "Investimento - Refrigeração/Ar-condicionado",
    "rotulo": "22405 - Investimento - Refrigeração/Ar-condicionado",
    "macro": "4 - INVESTIMENTOS",
    "grupo": "224 - Despesa Variável - Investimentos",
    "responsavel": "Diretoria"
  },
  {
    "codigo": "22406",
    "nome": "Investimento - Mobiliário/Decoração",
    "rotulo": "22406 - Investimento - Mobiliário/Decoração",
    "macro": "4 - INVESTIMENTOS",
    "grupo": "224 - Despesa Variável - Investimentos",
    "responsavel": "Diretoria"
  },
  {
    "codigo": "22407",
    "nome": "Investimento - Consultorias e Prestações de Serviços",
    "rotulo": "22407 - Investimento - Consultorias e Prestações de Serviços",
    "macro": "4 - INVESTIMENTOS",
    "grupo": "224 - Despesa Variável - Investimentos",
    "responsavel": "Diretoria"
  },
  {
    "codigo": "22408",
    "nome": "Investimento - Marcas e Patentes",
    "rotulo": "22408 - Investimento - Marcas e Patentes",
    "macro": "4 - INVESTIMENTOS",
    "grupo": "224 - Despesa Variável - Investimentos",
    "responsavel": "Diretoria"
  },
  {
    "codigo": "22409",
    "nome": "Investimento - Novas Unidades (Custos com novas lojas Boah)",
    "rotulo": "22409 - Investimento - Novas Unidades (Custos com novas lojas Boah)",
    "macro": "4 - INVESTIMENTOS",
    "grupo": "224 - Despesa Variável - Investimentos",
    "responsavel": "Diretoria"
  },
  {
    "codigo": "22409",
    "nome": "Investimento - Novas Unidades (Custos com novas lojas Boah)",
    "rotulo": "22409 - Investimento - Novas Unidades (Custos com novas lojas Boah)",
    "macro": "4 - INVESTIMENTOS",
    "grupo": "224 - Despesa Variável - Investimentos",
    "responsavel": "Diretoria"
  },
  {
    "codigo": "22501",
    "nome": "Retirada de Sócios",
    "rotulo": "22501 - Retirada de Sócios",
    "macro": "5 - RETIRADA SOCIO",
    "grupo": "225 - Despesa Variável - Retirada de Sócios",
    "responsavel": "Diretoria"
  }
];
