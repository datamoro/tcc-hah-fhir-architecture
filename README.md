# Arquitetura Distribuída para Monitoramento Fisiológico no Modelo Hospital-at-Home

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Apache Kafka](https://img.shields.io/badge/kafka-7.5.0-black.svg)](https://kafka.apache.org/)
[![TimescaleDB](https://img.shields.io/badge/timescaledb-pg14-orange.svg)](https://www.timescale.com/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![HL7 FHIR R4](https://img.shields.io/badge/HL7_FHIR-R4-red.svg)](https://hl7.org/fhir/R4/)
[![Docker](https://img.shields.io/badge/docker-compose-blue.svg)](https://docs.docker.com/compose/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **TCC — MBA em Engenharia de Software | ESALQ/USP**  
> **Autor:** Caio Moro  
> **Orientador:** Prof. Lucas José de Souza

---

## 📋 Sobre o Projeto

Este repositório contém a implementação de uma **arquitetura de software distribuída, orientada a eventos e compatível com o padrão HL7 FHIR**, desenvolvida como Trabalho de Conclusão de Curso (TCC) do MBA em Engenharia de Software da ESALQ/USP.

O objetivo é demonstrar a **viabilidade técnica** de uma infraestrutura open source para ingestão, transformação semântica e exposição de dados fisiológicos em contexto simulado do modelo assistencial **Hospital-at-Home (HaH)** — onde pacientes são monitorados remotamente em seus domicílios.

---

## 🏗️ Arquitetura

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐     ┌─────────────────┐     ┌──────────────┐
│  Sensor          │────▶│ Apache Kafka │────▶│  Worker FHIR     │────▶│  TimescaleDB    │────▶│  FastAPI     │
│  Simulator       │     │ (Mensageria) │     │  (Transformação) │     │  (Persistência) │     │  REST API    │
│  (Producer.py)   │     │ raw-sensor-  │     │  fhir.resources  │     │  Hypertable     │     │  /fhir/...   │
│                  │     │ data topic   │     │  LOINC codes     │     │  JSONB store    │     │  Swagger UI  │
└─────────────────┘     └──────────────┘     └──────────────────┘     └─────────────────┘     └──────────────┘
```

**Sinais vitais mapeados para FHIR:**

| Sinal Vital | Código LOINC | Unidade (UCUM) |
|---|---|---|
| Frequência Cardíaca (FC) | 8867-4 | beats/minute (/min) |
| Oximetria de Pulso (SpO2) | 59408-5 | % |
| Pressão Arterial (PA) | 55284-4 | mmHg (component) |

---

## 🛠️ Stack Tecnológico

| Componente | Tecnologia | Versão |
|---|---|---|
| Linguagem | Python | 3.12+ |
| Mensageria | Apache Kafka (Confluent Platform) | 7.5.0 |
| Coordenação | Apache ZooKeeper | 7.5.0 |
| Banco de dados | TimescaleDB (PostgreSQL) | pg14 |
| Framework API | FastAPI + Uvicorn | latest |
| Padrão Clínico | HL7 FHIR R4 (`fhir.resources`) | ≥7.0.0 |
| Orquestração | Docker & Docker Compose | - |
| ORM | SQLAlchemy + psycopg2 | - |

---

## 🚀 Como Rodar (One-Click)

### Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e em execução
- [Python 3.12+](https://www.python.org/downloads/) (para rodar os scripts localmente)
- Git

### 1. Clonar o repositório

```bash
git clone https://github.com/datamoro/tcc-hah-fhir-architecture.git
cd tcc-hah-fhir-architecture
```

### 2. Iniciar a infraestrutura

```bash
docker-compose up -d
```

Aguarde ~30 segundos para o Kafka e o TimescaleDB inicializarem completamente.

**Serviços disponíveis:**
- **Kafka UI:** http://localhost:8080 — monitoramento do cluster e tópicos
- **TimescaleDB:** `localhost:5432` — banco de dados (user: `postgres`, pass: `password`, db: `tcc_health`)

### 3. Instalar dependências Python

```bash
pip install -r requirements.txt
```

### 4. Verificar conectividade Kafka

```bash
python check_kafka.py
```

### 5. Iniciar o Worker FHIR (Transformação)

```bash
# Em um terminal separado
python -m app.transformation.worker
```

### 6. Iniciar o Simulador de Sensores (Ingestão)

```bash
# Em outro terminal
python -m app.ingestion.producer
```

### 7. Iniciar a API REST

```bash
uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000
```

**API disponível em:** http://localhost:8000  
**Documentação interativa (Swagger):** http://localhost:8000/docs

---

## 📡 Endpoints da API

### `GET /fhir/Observation`

Retorna recursos FHIR `Observation` armazenados no banco de dados.

**Parâmetros de query:**

| Parâmetro | Descrição | Exemplo |
|---|---|---|
| `patient` | Filtrar por ID de paciente | `P001` ou `Patient/P001` |
| `code` | Filtrar por código LOINC | `8867-4` (frequência cardíaca) |

**Exemplo de requisição:**
```bash
curl "http://localhost:8000/fhir/Observation?patient=P001&code=8867-4"
```

**Exemplo de resposta (FHIR R4 Observation):**
```json
{
  "resourceType": "Observation",
  "status": "final",
  "code": {
    "coding": [{
      "system": "http://loinc.org",
      "code": "8867-4",
      "display": "Heart rate"
    }]
  },
  "subject": { "reference": "Patient/P001" },
  "effectiveDateTime": "2026-04-15T16:00:00+00:00",
  "valueQuantity": {
    "value": 72,
    "unit": "beats/minute",
    "system": "http://unitsofmeasure.org",
    "code": "/min"
  },
  "device": { "display": "wearable-P001" }
}
```

---

## 📁 Estrutura do Repositório

```
tcc-hah-fhir-architecture/
│
├── app/
│   ├── ingestion/
│   │   └── producer.py          # Simulador de sensores (Kafka Producer)
│   ├── transformation/
│   │   └── worker.py            # Worker FHIR (Kafka Consumer + mapeamento LOINC)
│   ├── api/
│   │   ├── main.py              # FastAPI application
│   │   └── routers/
│   │       └── observations.py  # Endpoint /fhir/Observation
│   └── shared/
│       └── database.py          # Modelos SQLAlchemy + TimescaleDB hypertable
│
├── docs/
│   ├── Projeto_Executivo.md           # Visão técnica e roadmap
│   ├── Draft_Resultados_Preliminares.md  # Rascunho da seção de Resultados (TCC)
│   ├── Plano_Trabalho_Final.md         # Plano de trabalho para conclusão
│   ├── ToDo_Elaboracao_TCC.md          # To-do list da elaboração textual
│   └── Trello_Cards_TCC.md             # Cards sugeridos para gestão (Trello)
│
├── docker-compose.yml           # Infraestrutura (Kafka, ZooKeeper, TimescaleDB, Kafka UI)
├── requirements.txt             # Dependências Python
├── check_kafka.py               # Script de verificação de conectividade
└── .gitignore
```

---

## 🔬 Contexto Acadêmico

### Problema

O modelo assistencial **Hospital-at-Home (HaH)** viabiliza cuidados hospitalares agudos no domicílio do paciente. Sua implementação exige uma infraestrutura digital capaz de processar fluxos contínuos de dados fisiológicos de dispositivos vestíveis, mantendo integridade, rastreabilidade e conformidade com padrões de interoperabilidade.

### Solução Proposta

Uma arquitetura distribuída orientada a eventos que:
1. **Ingere** dados fisiológicos simulados via Apache Kafka
2. **Transforma** semanticamente os dados para o padrão HL7 FHIR R4 (recursos `Observation`)
3. **Persiste** os recursos FHIR em TimescaleDB com suporte a séries temporais
4. **Expõe** os dados via API RESTful compatível com FHIR Search

### Contribuição Científica

- Referência técnica **open source e replicável** de arquitetura FHIR para ambientes de monitoramento domiciliar
- Demonstração prática de mapeamento semântico com códigos LOINC e unidades UCUM
- Pipeline completo executável com único comando (`docker-compose up`)

---

## ⚠️ Limitações (MVP)

- Dados sintéticos (gerados por simulador); integração com PhysioNet/MIMIC-IV prevista como trabalho futuro
- API sem autenticação (SMART on FHIR / OAuth 2.0 previsto como trabalho futuro)
- Ambiente de execução local; deploy em nuvem não contemplado nesta versão

---

## 📚 Referências Principais

- Lins, L.F.A. et al. (2024). Interoperabilidade entre sistemas de informação em saúde: desafios e tendências com HL7 FHIR. *Revista Contemporânea.*
- Newman, S. (2015). *Building Microservices: Designing Fine-Grained Systems.* O'Reilly Media.
- Pandit, J.A. et al. (2024). The hospital at home in the USA: current status and future prospects. *NPJ Digital Medicine.*
- Vorisek, C.N. et al. (2022). Fast healthcare interoperability resources (FHIR) for interoperability in health research. *JMIR Medical Informatics.*
- Le, T.K.H. et al. (2024). Enhancing real-time clinical decision-making through AI-integrated FHIR solutions. *ICNGN 2024.*

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

*Trabalho desenvolvido como requisito parcial para obtenção do título de MBA em Engenharia de Software pela ESALQ/USP.*
