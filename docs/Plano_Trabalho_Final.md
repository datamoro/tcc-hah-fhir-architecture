# Plano de Trabalho Final — TCC Caio Moro
### Deadline: 21/04/2026 | Hoje: 15/04/2026 | Disponível: ~18 horas (3h/dia × 6 dias)

---

> [!CAUTION]
> Com apenas 6 dias disponíveis, este plano adota uma estratégia de **escopo mínimo viável para entrega**.
> Algumas tarefas técnicas planejadas anteriormente (dataset PhysioNet real, SMART on FHIR) são **descartadas** desta sprint final — serão mencionadas como trabalhos futuros no texto.

---

## 📊 Diagnóstico Atual (15/04)

| Componente | Status | Decisão |
|---|---|---|
| Código: Kafka + produtor | ✅ Funcional | Manter, documentar |
| Código: Worker FHIR (FC) | ✅ Funcional | Expandir SpO2 + PA |
| Código: TimescaleDB + API | ✅ Funcional | Manter, testar |
| Template ESALQ preenchido | ❌ Não existe | **Prioridade máxima** |
| Introdução | ✅ Texto pronto | Copiar para template |
| Metodologia | 🟡 Esboço no proj. pesquisa | Expandir e finalizar |
| Resultados e Discussão | 🟡 Draft exists | Expandir e finalizar |
| Conclusão | ❌ Não existe | Redigir |
| Resumo / Abstract | ❌ Não existe | Redigir |
| Referências | 🟡 Parcial | Completar e formatar |
| GitHub público | ❌ Não publicado | Publicar |
| Diagrama arquitetura | ❌ Não existe | Criar (simples) |
| Validação FHIR oficial | ❌ Não feita | Fazer e capturar print |
| Submissão na plataforma | ❌ Não feita | Entrega final |

---

## 🗓️ Plano Dia a Dia

---

### DIA 1 — 15/04 (Terça) — "Código e Template"
**Meta:** Fechar o código e abrir o template preenchido com Introdução + cabeçalho.

**Bloco 1 — 1h (Código)**
- [ ] Implementar mapeamento FHIR para **SpO2** no `worker.py` (LOINC 59408-5, unit `%`)
- [ ] Implementar mapeamento FHIR para **Pressão Arterial** no `worker.py` (LOINC 55284-4, usando `component`)
- [ ] Testar os 3 sinais ponta a ponta: subir `docker-compose`, executar produtor + worker + API

**Bloco 2 — 1h (Documentação)**
- [ ] Abrir `Template/Template TCC_PT.docx`
- [ ] Preencher cabeçalho: título, Caio Moro, Prof. Lucas José de Souza, e-mail
- [ ] Colar e ajustar a **Introdução** (texto já pronto — remover "segurança" do objetivo, qualificar "tempo quase real" como "em contexto simulado")

**Bloco 3 — 1h (Diagrama)**
- [ ] Criar **Figura 1** — diagrama do pipeline (usar draw.io, Excalidraw ou PowerPoint)
  - Fluxo: Sensor Simulado → Kafka → Worker FHIR → TimescaleDB → FastAPI → Cliente
  - Exportar como PNG

---

### DIA 2 — 16/04 (Quarta) — "Metodologia"
**Meta:** Seção Metodologia finalizada no template.

**Bloco 1 — 1h (Escrita)**
- [ ] Redigir parágrafo 1: Caracterização da pesquisa (estudo de caso tecnológico, dados simulados)
- [ ] Redigir parágrafo 2: Ambiente e ferramentas (Docker, versões: Kafka 7.5.0 CP, TimescaleDB pg14, Python 3.12+, libs do requirements.txt)
- [ ] Redigir parágrafo 3: Fonte de dados — justificar uso de dados sintéticos gerados programaticamente como representação de leituras de wearables; mencionar PhysioNet como fonte de referência dos intervalos fisiológicos adotados

**Bloco 2 — 1h (Escrita)**
- [ ] Redigir parágrafo 4: Pipeline de ingestão e mensageria — Kafka, tópico `raw-sensor-data`, estrutura da mensagem JSON
- [ ] Redigir parágrafo 5: Transformação FHIR — biblioteca `fhir.resources`, recursos `Observation`, 3 códigos LOINC, validação Pydantic
- [ ] Redigir parágrafo 6: Persistência e exposição — TimescaleDB (hypertable), FastAPI, endpoint `/fhir/Observation`

**Bloco 3 — 1h (Escrita + Revisão)**
- [ ] Redigir parágrafo 7: Estratégia de validação — validador oficial FHIR, métricas de latência registradas
- [ ] Revisar toda a seção: pretérito perfeito, forma impessoal
- [ ] Colar no template

---

### DIA 3 — 17/04 (Quinta) — "Resultados e Validação"
**Meta:** Seção Resultados finalizada + evidências coletadas.

**Bloco 1 — 1h (Coleta de evidências)**
- [ ] Com docker-compose rodando:
  - Registrar **tempo de resposta** do endpoint (`curl -w "%{time_total}"` ou Postman)
  - Capturar screenshot da **Kafka UI** (tópico com mensagens)
  - Capturar screenshot da **Swagger UI** (http://localhost:8000/docs)
  - Copiar 1 exemplo de JSON FHIR retornado pela API
- [ ] Submeter recurso FHIR em **https://validator.fhir.org/** → capturar screenshot do resultado

**Bloco 2 — 1.5h (Escrita)**
- [ ] Expandir o `Draft_Resultados_Preliminares.md` com:
  - Atualizar 3.2 para incluir SpO2 e PA
  - Inserir bloco de código JSON de exemplo na seção 3.4
  - Criar Tabela 1: métricas de latência registradas (ex: tempo médio de resposta da API)
  - Referenciar Figura 1 (diagrama)
- [ ] Comparar resultados de latência com Le et al. (2024): 50-300ms

**Bloco 3 — 0.5h (Template)**
- [ ] Colar seção Resultados no template
- [ ] Inserir Figura 1 e screenshots como figuras numeradas

---

### DIA 4 — 18/04 (Sexta) — "Conclusão + Resumo + GitHub"
**Meta:** Texto 100% no template. Repositório publicado.

**Bloco 1 — 1h (Escrita: Conclusão)**
- [ ] Redigir Conclusão (frases curtas, sem tabelas, sem citações de terceiros):
  - Retomar o objetivo declarado na Introdução
  - Confirmar que foi demonstrada a viabilidade técnica da arquitetura para HaH
  - Listar contribuições: pipeline open source, conformidade FHIR, replicabilidade com Docker
  - Mencionar limitações: dados sintéticos, ausência de autenticação, escala não testada em produção
  - Mencionar trabalhos futuros: integração PhysioNet real, SMART on FHIR, deploy em nuvem

**Bloco 2 — 1h (Escrita: Resumo + Abstract)**
- [ ] Redigir Resumo (máx. 250 palavras, 1 parágrafo, pretérito perfeito):
  - Contextualização → Objetivo → Metodologia → Resultados → Conclusão
- [ ] Definir 5 palavras-chave (diferentes do título)
- [ ] Traduzir Resumo para inglês (Abstract) — opcional mas recomendado

**Bloco 3 — 1h (GitHub)**
- [ ] Verificar se o repositório `product/.git` tem remote configurado
- [ ] Atualizar `README.md` com: descrição, pré-requisitos, como rodar (docker-compose up + scripts)
- [ ] Commit e push de tudo
- [ ] Tornar repositório **público**
- [ ] Copiar URL do GitHub para citar no texto do TCC (Apêndice ou Referências)

---

### DIA 5 — 19/04 (Sábado) — "Referências + Revisão Geral"
**Meta:** Documento completo e revisado.

**Bloco 1 — 1h (Referências)**
- [ ] Listar TODAS as citações feitas no texto do template
- [ ] Formatar cada referência conforme norma ESALQ/USP (checar Manual de Normas)
- [ ] Adicionar referências faltantes:
  - Kafka: Apache Software Foundation (docs oficiais)
  - TimescaleDB: Timescale Inc. (docs oficiais)
  - FastAPI: Ramírez (criador / docs)
  - PhysioNet: Goldberger et al. (2000) — referência padrão da plataforma

**Bloco 2 — 1h (Revisão técnica)**
- [ ] Verificar limite de páginas (máx. 30 incluindo apêndices)
- [ ] Verificar: todas as figuras estão numeradas e referenciadas no texto?
- [ ] Verificar: todas as tabelas estão numeradas?
- [ ] Conferir formatação do template (fonte, espaçamento, margens)

**Bloco 3 — 1h (Revisão de conteúdo)**
- [ ] Reler introdução → verificar se a promessa de "segurança" foi removida/qualificada
- [ ] Reler metodologia → está coerente com o código implementado?
- [ ] Reler resultados → todas as evidências (prints, JSONs, tabela de latência) estão no texto?
- [ ] Reler conclusão → responde o objetivo? Não cita resultados de terceiros?

---

### DIA 6 — 20/04 (Domingo) → 21/04 (Segunda) — "Entrega"
**Meta:** Submissão na plataforma + buffer para imprevistos.

**20/04 (1h)**
- [ ] Ajustes finais apontados na revisão do dia anterior
- [ ] Salvar versão final com nome: `TCC_CaioMoro_vFinal.docx`
- [ ] Converter para PDF (verificar se a plataforma aceita PDF ou só .docx)

**21/04 (1h)**
- [ ] **SUBMETER** o arquivo na plataforma ESALQ/USP
- [ ] Confirmar recebimento / protocolo de entrega
- [ ] Enviar e-mail ao orientador informando a submissão (com link do GitHub)

---

## 🚫 O que está FORA DO ESCOPO desta sprint (mencionar como trabalho futuro)

| Item | Motivo do corte |
|---|---|
| Dataset PhysioNet real | Requires setup demorado, não muda a validade arquitetural |
| Autenticação SMART on FHIR / OAuth2 | Complexidade alta, 6 dias insuficientes |
| Testes de carga (stress test) | Sem tempo para setup e análise adequada |
| Deploy em nuvem (AWS/GCP) | Fora do escopo original do MVP |

---

## ✅ Critério de Sucesso

O TCC estará pronto para entrega quando:
1. O arquivo `.docx` no template ESALQ tiver todas as seções preenchidas
2. A Figura 1 (diagrama) e pelos menos 1 print de evidência estiverem no texto
3. O repositório GitHub estiver público e citado no trabalho
4. O arquivo estiver submetido na plataforma e o orientador notificado
