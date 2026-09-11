# 📋 Caderno de Briefing & Melhorias do Bimer Cloud

Documento vivo de acompanhamento dos testes, ajustes, melhorias e solicitações do gestor **Roberto** durante o uso prático da plataforma.

---

## 📌 Status Atual do Sistema (Baseline)
* **Ambiente:** Bimer Cloud (Frontend PWA + Backend FastAPI + Turso Cloud AWS)
* **Base de Dados Ativa:** 45 títulos consolidados (R$ 55.339,47) e 115 fornecedores/colaboradores cadastrados.
* **Últimos Ajustes Concluídos:**
  - [x] Seleção inteligente de data nos relatórios de Autorização da Diretoria e Folha do Dia (abre diretamente no lote com maior volume em aberto).
  - [x] Criação das opções nativas: `🛍️ Domingo / Feriado Trabalhado (Individual)` e `👥 Folha de Pagamento / Salários (Total Consolidado)`.
  - [x] Integração e sincronização dos 32 lançamentos do borderô (Cataguases, Têxtil Suíça, Brand, faccionistas e vendedoras).
  - [x] Automação do cadastro de fornecedores no ato do lançamento.
  - [x] Paridade binária garantida entre os espelhos HTML.
  - [x] Catálogo ampliado de CNAEs oficiais (51 atividades segmentadas: Confecção, Ateliê, Lookbook, Logística, Manutenção, TI e Saúde Ocupacional).
  - [x] Implementação do Novo Padrão Tributário Nacional (Reforma Tributária • EC 132/2023 - IVA Dual: CBS 0,90% Federal + IBS 0,10% Subnacional + CTN).

---

## 📝 Fila de Melhorias, Ajustes & Feedbacks (Em Teste)

| # | Módulo / Tela | Descrição do Ponto / Ajuste | Impacto / Prioridade | Status |
| :-: | :--- | :--- | :---: | :---: |
| 1 | Fiscal / Tributos | Catálogo oficial de 51 CNAEs com filtros por segmento (Moda, Foto, Manutenção, Frete, TI) | Alto (Usabilidade) | ✅ Concluído |
| 2 | Fiscal / NFS-e | Painel do Novo Padrão Tributário (IBS 0,10% + CBS 0,90% + CTN) em tempo real | Alto (Conformidade 2026) | ✅ Concluído |
| 3 | Fiscal / Tributos | Inclusão de CNAEs de Serviços Técnicos em Eletrônica e Eletrotécnica (7112-0/00, 3313-9/99, 3312-1/02, 9521-5/00) e Item 31.01 LC 116 | Alto (Atendimento) | ✅ Concluído |
| 4 | Contas a Pagar / Cadastros | Atualização dos CPFs completos das faccionistas (Claudice, Flavia, Barbara, Juvanice) e exclusão dos lançamentos com asterisco (Carolina e Eduardo) | Alto (Integridade Cadastral) | ✅ Concluído |
| 5 | Contas a Pagar (Aba 3) | Separação visual de Títulos em Aberto e Baixados por Sub-Abas, remoção de botões redundantes e inclusão de busca instantânea em tempo real | Alto (UX / Produtividade) | ✅ Concluído |
| 6 | Contas a Pagar (Aba 3) | Unificação do filtro 'Folha, Domingos & Feriados Trabalhados', remoção do filtro redundante de prestador e implementação de Classificação / Ordenação em todas as colunas | Alto (Usabilidade & Análise) | ✅ Concluído |
| 7 | Global / UI & Design | Substituição completa de emojis amadores por ícones vetoriais SVG corporativos (estilo Lucide/Alterdata ERP) em todo o sistema, sem emojis residuais | Alto (Qualidade Visual & Profissionalismo) | ✅ Concluído |

---

## 🎯 Diretrizes de Desenvolvimento
1. **Preservação Visual:** Manter rigorosamente o layout e a paleta de cores corporativa do Alterdata Bimer.
2. **Sincronia Absoluta:** Qualquer alteração no frontend deve ser refletida de forma idêntica nos espelhos `prototipo_contas_a_pagar.html`.
3. **Persistência Dupla:** Toda gravação deve garantir consistência entre o SQLite local e o Turso Cloud na AWS.
