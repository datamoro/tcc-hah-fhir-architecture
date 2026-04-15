# 🗂️ Trello Board — PROJETO TCC
## Arquitetura Distribuída para Monitoramento Fisiológico no Modelo Hospital-at-Home

> **Deadline final:** 15/03/2026 | **Hoje:** 23/02/2026 | **Dias disponíveis:** 20 dias

---

## 🔵 DONE — Já concluídos (mover imediatamente para Done)

| # | Título | Descrição |
|---|--------|-----------|
| D1 | **Levantamento Bibliográfico** | 27 artigos coletados na pasta `estudo bibliografico/`, cobrindo FHIR, HaH, microsserviços, TimescaleDB e interoperabilidade. |
| D2 | **Projeto de Pesquisa Oficial** | Projeto aprovado, entregue e registrado na plataforma ESALQ/USP. |
| D3 | **Escopo Técnico Definido** | Arquitetura definida: Kafka + FHIR + TimescaleDB + FastAPI em Docker. |
| D4 | **Infraestrutura Docker (docker-compose.yml)** | Kafka, ZooKeeper, TimescaleDB, Kafka UI configurados e funcionando. |
| D5 | **Produtor Kafka — Simulador de Sensores** | `app/ingestion/producer.py` simula sinais vitais (FC, SpO2, PA) de 3 pacientes. |
| D6 | **Worker de Transformação FHIR (FC)** | `app/transformation/worker.py` mapeia freq. cardíaca (LOINC 8867-4) para recurso FHIR `Observation`. |
| D7 | **Modelo de Dados TimescaleDB** | `app/shared/database.py`: tabela `fhir_observations` com hypertable e coluna JSONB. |
| D8 | **API FastAPI — Endpoint /fhir/Observation** | `app/api/routers/observations.py` expõe recursos FHIR com filtros por `patient` e `code`. |
| D9 | **Repositório Git Inicializado** | Projeto versionado localmente com `.gitignore` configurado. |
| D10 | **Termo de Prorrogação Assinado** | Documento `Termo_de_Prorrogacao_de_Prazo_-_TCC_-_241.docx_%281%29_assinado.pdf` já arquivado. |

---

## 🟠 TO-DO (prioridade máxima — iniciar hoje)

### 📄 Documentação & Template

| # | Título | Descrição | Prazo |
|---|--------|-----------|-------|
| T1 | **Migrar conteúdo para o Template Oficial ESALQ** | Abrir `Template TCC_PT.docx`, copiar Introdução e Objetivo do Projeto de Pesquisa e colar/adaptar às normas do template. Preencher cabeçalho completo. | **25/02** |
| T2 | **Submeter rascunho na plataforma de TCCs** | Mesmo que incompleto, enviar o arquivo `.docx` na plataforma para registrar progresso e cumprir formalidade pendente. | **25/02** |
| T3 | **Redigir o Resumo (máx. 250 palavras)** | Seguir estrutura: contextualização → objetivo → metodologia → resultados → conclusão. Redigir em pretérito perfeito, parágrafo único. | **26/02** |
| T4 | **Revisar e finalizar seção Introdução** | Adaptar texto do Projeto de Pesquisa: checar citações, atualizar links, garantir objetivo no último parágrafo. Checar limite de 2 páginas. | **26/02** |
| T5 | **Redigir seção Metodologia** | Baseado no escopo v1 e projeto de pesquisa: detalhar ambiente Docker (versões), lib versions (`requirements.txt`), pipeline FHIR, estratégia de dados (PhysioNet). Pretérito perfeito, impessoal. | **28/02** |
| T6 | **Expandir e finalizar Resultados e Discussão** | Usar o Draft em `Draft_Resultados_Preliminares.md` como base. Conter: diagrama de arquitetura, exemplo de output JSON da API, tabela de latência. Comparar com literatura (Le et al., 2024). | **05/03** |
| T7 | **Redigir Conclusão** | Frases curtas, responder ao objetivo. Contribuições: referência open source FHIR para HaH. Limitações. Perspectivas futuras. Sem tabelas/figuras/citações de terceiros. | **08/03** |
| T8 | **Verificar e formatar Referências** | Conferir todas as referências citadas no texto final versus lista disponível. Formatar conforme norma ESALQ/USP. Adicionar referências de TimescaleDB, Kafka, FastAPI, PhysioNet. | **10/03** |
| T9 | **Revisão final do documento (.docx)** | Checar formatação total no template, paginação, limite de 30 páginas, normas ESALQ. Revisar ortografia e coesão. | **13/03** |
| T10 | **Submissão final na plataforma** | Enviar versão definitiva do `.docx` no Sistema de TCCs ESALQ/USP. | **15/03** |

---

## 🟡 BACKLOG — Técnico (implementar para embasar os Resultados)

| # | Título | Descrição | Prazo |
|---|--------|-----------|-------|
| B1 | **Implementar mapeamento FHIR — SpO2** | Adicionar ao `worker.py` a criação do recurso `Observation` para SpO2 com LOINC 59408-5 e unidade `%`. Dados já chegam no tópico Kafka. | **26/02** |
| B2 | **Implementar mapeamento FHIR — Pressão Arterial** | Adicionar ao `worker.py` o mapeamento para PA sistólica/diastólica com LOINC 55284-4, usando `component` do recurso FHIR (BP tem dois valores). | **27/02** |
| B3 | **Integrar dataset PhysioNet (amostra)** | Baixar amostra do MIMIC-IV Waveform ou MIMIC-IV Clinical. Criar script que leia o CSV e o envie para o Kafka em substituição ao gerador aleatório. | **02/03** |
| B4 | **Criar diagrama de arquitetura (Figura 1)** | Produzir diagrama visual do fluxo completo: Sensor → Kafka → Worker FHIR → TimescaleDB → FastAPI. Usar draw.io, Excalidraw ou Mermaid. Exportar em PNG/SVG para o TCC. | **01/03** |
| B5 | **Executar e documentar teste de latência** | Medir latência do pipeline ponta a ponta: produtor → API. Registrar throughput (msg/s) e tempo de resposta do endpoint. Criar tabela com os resultados para o TCC. | **04/03** |
| B6 | **Validar recursos FHIR com validador oficial** | Copiar o JSON de uma `Observation` gerada e submeter em [validator.fhir.org](https://validator.fhir.org/). Capturar screenshot do resultado como evidência no TCC. | **03/03** |

---

## 🔵 DESIGN

| # | Título | Descrição | Prazo |
|---|--------|-----------|-------|
| DE1 | **Definir perfis FHIR para os 3 sinais vitais** | Documentar formalmente os perfis FHIR utilizados: campos obrigatórios, codes LOINC, unidades UCUM (unified code for units of measure), referências de Patient e Device. | **25/02** |
| DE2 | **Criar diagrama BPMN do pipeline** | Representar o fluxo de dados em BPMN 2.0 para incluir no TCC como artefato metodológico. Mostra: geração de dado → publicação Kafka → consumo → transformação → persistência → consulta API. | **01/03** |
| DE3 | **Modelar esquema de Apêndice** | Definir o que irá no Apêndice do TCC: código-fonte relevante, diagrama de arquitetura, tabela de testes, exemplos de JSON FHIR. Planejar dentro do limite de 30 páginas totais. | **03/03** |

---

## 🟢 CODE REVIEW

| # | Título | Descrição | Prazo |
|---|--------|-----------|-------|
| CR1 | **Revisar `worker.py` após expansão dos 3 sinais** | Após implementar SpO2 e PA (B1, B2), revisar o código do worker: tratamento de exceções, logging, organização em funções. | **28/02** |
| CR2 | **Publicar repositório no GitHub (público)** | Garantir que o repositório esteja público, com `README.md` completo (instruções de uso, diagrama, pré-requisitos). Este é um entregável do TCC. | **05/03** |
| CR3 | **Revisar `docker-compose.yml`** | Checar se todos os serviços sobem corretamente, healthchecks, variáveis de ambiente separadas em `.env`. Garantir "one-click run" conforme prometido no projeto. | **27/02** |

---

## 🔴 TESTING

| # | Título | Descrição | Prazo |
|---|--------|-----------|-------|
| TE1 | **Teste end-to-end do pipeline completo** | Subir todos os contêineres, executar produtor, verificar que o worker consome, transforma e persiste os 3 sinais vitais. Consultar via API e confirmar retorno FHIR válido. | **04/03** |
| TE2 | **Teste de carga (stress test básico)** | Aumentar frequência do produtor (ex: 100 msg/s) e medir comportamento do sistema: presença de lag Kafka, latência de persistência, tempo de resposta da API sob carga. | **05/03** |
| TE3 | **Validação FHIR R4 com validator oficial** | Referente à B6. Registrar resultado: % de conformidade, warnings, erros. Documentar no TCC as correções aplicadas. | **03/03** |

---

## 📊 Cronograma Resumido (20 dias)

```
Fev 23 ──────── Mar 01 ──────── Mar 08 ──────── Mar 15
  │                │                │                │
  ├─ T1/T2: Template + Submissão inicial
  ├─ B1/B2: SpO2 + PA no worker
  ├─ DE1: Perfis FHIR documentados
  │                │
                   ├─ B3: Dataset PhysioNet
                   ├─ B4: Diagrama arquitetura
                   ├─ CR3: docker-compose revisado
                   ├─ T5: Metodologia redigida
                   │                │
                                    ├─ B5/TE2: Testes de carga
                                    ├─ B6/TE3: Validação FHIR
                                    ├─ T6: Resultados finalizados
                                    ├─ CR2: GitHub público
                                    │                │
                                                     ├─ T7: Conclusão
                                                     ├─ T8: Referências
                                                     ├─ T9: Revisão final
                                                     └─ T10: SUBMISSÃO FINAL ✅
```
