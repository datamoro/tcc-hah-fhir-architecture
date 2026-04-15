# ✅ To-Do List — Elaboração Textual do TCC

> **Padrão obrigatório:** Template oficial ESALQ/USP (`Template TCC_PT.docx`)
> **Prazo de referência:** Verificar no Portal do Sistema de TCCs.

---

## 🔴 URGENTE — Fazer ANTES da reunião

- [ ] Baixar o template oficial da plataforma (ou usar o arquivo `Template TCC_PT.docx` já disponível).
- [ ] Migrar o texto do Projeto de Pesquisa (Introdução + Objetivo inicial) para o `.docx` do template.
- [ ] Preencher o cabeçalho do template: título, nome autor, orientador, e-mail.
- [ ] Submeter o arquivo (mesmo que incompleto) na plataforma de TCCs — isso resolve o problema da entrega em aberto.

---

## 📋 Seção 1 — Título

- [ ] Revisar o título atual: *"Arquitetura Distribuída para Monitoramento Fisiológico no Modelo Hospital-at-Home"*
  - ✅ Tem menos de 15 palavras — OK.
  - ✅ Não contém expressões proibidas ("Estudo de...", "Análise de...") — OK.
  - [ ] Considerar adicionar "HL7 FHIR" ao título para evidenciar a contribuição técnica principal.

---

## 📋 Seção 2 — Resumo (máx. 250 palavras, 1 parágrafo)

- [ ] Redigir o Resumo seguindo a estrutura obrigatória:
  - [ ] Contextualização (2-3 frases): desafio da interoperabilidade no HaH.
  - [ ] Objetivo geral (1 frase): desenvolvimento de arquitetura distribuída FHIR para HaH.
  - [ ] Metodologia (2-3 frases): pipeline Kafka + FHIR + TimescaleDB + FastAPI, dados PhysioNet.
  - [ ] Principais resultados (2-3 frases): MVP funcional, validação semântica FHIR, estrutura open source.
  - [ ] Conclusão geral (1-2 frases): contribuição para saúde digital / HaH.
- [ ] Verificar contagem de palavras (máx. 250).
- [ ] Escrever em pretérito perfeito do indicativo.
- [ ] Inserir até 5 palavras-chave diferentes das do título (ex: "interoperabilidade; microsserviços; sinais vitais; mensageria assíncrona; saúde digital").
- [ ] Traduzir Resumo para inglês (Abstract) — opcional, mas recomendado.

---

## 📋 Seção 3 — Introdução (máx. 2 páginas, sem subtópicos)

- [ ] ✅ Texto base já existe no Projeto de Pesquisa — copiar e adaptar.
- [ ] Revisar e atualizar referências (verificar datas de acesso e disponibilidade dos links).
- [ ] Garantir que o último parágrafo enuncia claramente o objetivo do trabalho.
- [ ] Remover subtópicos (a introdução não pode ter subdivisões).
- [ ] Checar limite de 2 páginas no template.

---

## 📋 Seção 4 — Metodologia ou Material e Métodos

- [ ] ✅ Estrutura base já existe no Projeto de Pesquisa — expandir com detalhes técnicos reais.
- [ ] Detalhar o ambiente de desenvolvimento:
  - [ ] Especificações do ambiente Docker (versão Kafka, TimescaleDB, ZooKeeper).
  - [ ] Versão Python, bibliotecas e versões (`requirements.txt` já existe no `/product`).
- [ ] Descrever a fonte de dados (PhysioNet):
  - [ ] Dataset selecionado (MIMIC-IV, MIMIC-Waveform, ou equivalent).
  - [ ] Processo de anonimização (já anonimizados por natureza).
- [ ] Descrever o processo de mapeamento FHIR:
  - [ ] Perfis FHIR utilizados (`Observation`, `Patient`, `Device`).
  - [ ] Códigos LOINC mapeados (8867-4 FC; 59408-5 SpO2; 55284-4 PA).
- [ ] Descrever a API e os critérios de validação de conformidade.
- [ ] Escrever em pretérito perfeito, forma impessoal.

---

## 📋 Seção 5 — Resultados e Discussão ⬅️ (DRAFT JÁ CRIADO)

- [ ] ✅ Draft inicial disponível em `Draft_Resultados_Preliminares.md`.
- [ ] Expandir seção 3.2: adicionar mapeamento de SpO2 e Pressão Arterial ao worker.
  - **Dependência de código**: implementar no `worker.py` antes de escrever.
- [ ] Expandir seção 3.4: adicionar exemplos de resposta JSON da API (screenshot ou bloco de código).
- [ ] Criar e inserir **Figura 1**: Diagrama da arquitetura (pode usar draw.io ou Mermaid).
- [ ] Executar e registrar um teste de latência básico (ex: tempo de resposta do endpoint `/fhir/Observation`).
- [ ] Comparar resultados com a literatura: Le et al. (2024) — 50ms a 300ms.
- [ ] Reescrever todo o draft em pretérito perfeito, terceira pessoa impessoal.
- [ ] Verificar citações inline (formato ESALQ/USP: Autor, Ano).

---

## 📋 Seção 6 — Conclusão(ões) ou Considerações Finais

- [ ] Redigir após a estabilização dos Resultados.
- [ ] Responder diretamente ao objetivo declarado na Introdução.
- [ ] Listar contribuições do projeto: referência técnica open source, validação do padrão FHIR em HaH.
- [ ] Mencionar limitações e perspectivas de continuidade.
- [ ] **NÃO** citar resultados de outros estudos nesta seção.
- [ ] **NÃO** incluir tabelas ou figuras.

---

## 📋 Seção 7 — Referências

- [ ] ✅ Referências base já existem no Projeto de Pesquisa.
- [ ] Verificar e completar todas as referências citadas nos novos capítulos.
- [ ] Formatar rigorosamente conforme normas ESALQ/USP.
- [ ] Adicionar referências faltantes sobre: TimescaleDB, Apache Kafka, FastAPI, PhysioNet.

---

## 🔧 Tarefas Técnicas com Impacto Direto no Texto

> Estas tarefas de código precisam ser concluídas **para que você tenha resultados reais a descrever**.

- [ ] **Implementar mapeamento FHIR para SpO2** (`worker.py`) — LOINC 59408-5.
- [ ] **Implementar mapeamento FHIR para Pressão Arterial** (`worker.py`) — LOINC 55284-4.
- [ ] **Integrar dataset PhysioNet**: substituir dados sintéticos por dados reais (mesmo que amostra pequena).
- [ ] **Executar e documentar teste de carga**: registrar throughput e latência (ex: 100, 1000, 10000 msg/s).
- [ ] **Executar validador oficial FHIR** (ex: [validator.fhir.org](https://validator.fhir.org/)): capturar screenshot como evidência.
- [ ] **Subir código ao GitHub**: tornar o repositório público com README completo.

---

## 📦 Entregáveis Finais

- [ ] Arquivo `.docx` no template oficial com todas as seções preenchidas.
- [ ] Repositório GitHub público com código, `docker-compose.yml`, e documentação.
- [ ] Diagrama de arquitetura (Figura 1) em alta resolução.
- [ ] Relatório/tabela de testes de desempenho e conformidade FHIR.
