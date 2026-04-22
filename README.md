# Hospital-at-Home (HaH) FHIR Architecture

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Async_REST-009688?style=flat&logo=fastapi)
![Kafka](https://img.shields.io/badge/Apache_Kafka-Message_Broker-black?style=flat&logo=apachekafka)
![Docker](https://img.shields.io/badge/Docker-Microservices-2496ED?style=flat&logo=docker)
![HL7 FHIR](https://img.shields.io/badge/HL7_FHIR-Release_5-E62D42?style=flat)
![CI](https://github.com/datamoro/tcc-hah-fhir-architecture/actions/workflows/main.yml/badge.svg)

Arquitetura distribuída open source para ingestão, transformação e exposição interoperável de sinais vitais de pacientes domiciliares no padrão **HL7 FHIR R5**, desenvolvida como TCC do MBA em Engenharia de Software (USP/Esalq).

---

## Arquitetura

```
Sensor Simulado → Apache Kafka → FHIR Worker → TimescaleDB → FastAPI → Cliente
   (producer.py)   (raw-sensor-data)  (worker.py)   (hypertable)  (8 workers async)
```

| Componente | Tecnologia | Função |
|---|---|---|
| **Producer** | Python + confluent-kafka | Simula 3 pacientes com FC, SpO2 e PA a 1 msg/s |
| **Broker** | Apache Kafka 7.5.0 | Desacopla ingestão e transformação |
| **Worker** | Python + fhir.resources | Mapeia sinais brutos → FHIR R5 Observation (LOINC) |
| **Banco** | TimescaleDB pg14 | Hypertable particionada por effective_datetime |
| **API** | FastAPI + asyncpg | 8 workers Uvicorn, endpoint async, serialização nativa FastAPI |
| **Auth** | JWT Bearer (SMART on FHIR mock) | Escopo patient/*.read obrigatório |

### Sinais Vitais Mapeados

| Sinal | LOINC | Recurso FHIR |
|---|---|---|
| Frequência Cardíaca | 8867-4 | Observation simples |
| SpO2 | 59408-5 | Observation simples |
| Pressão Arterial | 85354-9 / 8480-6 / 8462-4 | Observation com componentes |

---

## Como Executar

```bash
git clone https://github.com/datamoro/tcc-hah-fhir-architecture.git
cd tcc-hah-fhir-architecture
docker-compose up --build -d
```

Serviços disponíveis após ~30s:

| Serviço | URL |
|---|---|
| API (Swagger UI) | http://localhost:8000/docs |
| Kafka UI | http://localhost:8080 |

### Autenticação

```bash
curl -X POST http://localhost:8000/auth/token \
  -d "username=clinician&password=supersecure"
```

Use o `access_token` retornado como Bearer no header `Authorization`.

### Consulta FHIR

```bash
curl http://localhost:8000/fhir/Observation \
  -H "Authorization: Bearer <token>"
```

---

## Performance

Teste de estresse: 500 threads simultâneas | ramp-up 30s | carga sustentada 45s

| Endpoint | N | Mín | Mediana | P90 | Máx | Erros |
|---|---|---|---|---|---|---|
| /auth/token | 10.813 | 8 ms | 497 ms | 2.066 ms | 8.304 ms | 0% |
| /fhir/Observation | 10.799 | 11 ms | 483 ms | 1.971 ms | 9.448 ms | 0% |
| **TOTAL** | **21.612** | **8 ms** | **490 ms** | **2.017 ms** | **9.448 ms** | **0%** |

Throughput: **246,6 req/s** | Ambiente: hardware de desenvolvimento local (12 CPUs, Docker)

Benchmark de referência: Le et al. (2024) — 50–300 ms em carga operacional clínica típica.

---

## Qualidade e CI

```bash
# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt

# Rodar testes unitários (requer PostgreSQL local ou Docker)
pytest tests/unit/ -v
```

O pipeline de CI (GitHub Actions) executa a suíte completa a cada push com TimescaleDB provisionado como serviço.

---

## Estrutura do Repositório

```
app/
  ingestion/       # Producer Kafka (confluent-kafka)
  transformation/  # FHIR Worker (fhir.resources + asyncpg)
  api/             # FastAPI Gateway (async, JWT)
  shared/          # Engine síncrona (worker) + assíncrona (API)
tests/
  unit/            # Pytest: transformação FHIR + autenticação API
  run_jmeter_mock.py  # Script de carga (500 threads)
docs/
  Projeto_Executivo.md
  Otimizacao_Performance_API.md  # Guia de estudo sobre arquitetura async
```

---

*Artefato acadêmico — MBA Engenharia de Software, USP/Esalq. Autor: Caio Moro. Orientador: Prof. Lucas José de Souza.*
