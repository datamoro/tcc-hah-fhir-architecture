# Hospital-at-Home (HaH) FHIR Architecture

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Modern_REST-009688?style=flat&logo=fastapi)
![Kafka](https://img.shields.io/badge/Apache_Kafka-Message_Broker-black?style=flat&logo=apachekafka)
![Docker](https://img.shields.io/badge/Docker-Microservices-2496ED?style=flat&logo=docker)
![HL7 FHIR](https://img.shields.io/badge/HL7_FHIR-Release_5-E62D42?style=flat)

Arquitetura distribuída *Open Source* desenhada estruturalmente para escalonar a captação, ingestão e tradução universal de biometrias vestíveis de pacientes acamados remotamente para os moldes clínicos de interoperabilidade mundial da saúde, o **HL7 FHIR (Fast Healthcare Interoperability Resources)**.

Esta Prova de Conceito empacota um Data Pipeline interconectado e amarrado em *Microservices*, com blindagens de autenticação baseadas no protocolo SMART. Trata-se de um artefato acadêmico formatado ao longo da graduação de Engenharia de Software focada em saúde descentralizada inteligente do futuro.

---

## 🏛 Topologia e Componentes (Mesh)

A infraestrutura foi convertida com isolamento global agnóstico sendo estruturada assim:
- **`app/ingestion` (Gerador/Producer)**: Componentes responsáveis pela emulação orgânica dos sensores IoT imitando intervalos físicos vitais espelhados de algoritmos basais do [PhysioNet]. 
- **`Apache Kafka + Zookeeper`**: Um Event-broker que age como pulmão logístico, absorvendo picos imensos de biometria antes de sobrecarregar integrações analíticas.
- **`app/transformation` (FHIR Worker)**: Escravo de inteligência HL7 isolado. Aloca recursos Pydantic de `fhir.resources`, consumindo o Kafka tópico a tópico traduzindo os espectros sob três *LOINCs* restritos (Frequência `8867-4`, SpO2 `59408-5` e PA Sistética/Diastólica `85354-9`). 
- **`TimescaleDB`**: Motor relacional enxertado em PostgreSQL que constrói `Hypertables` massivas para leitura serial temporal clínica dos recursos em milissegundos.
- **`app/api` (FastAPI Cloud Gateway)**: Ponto focal de consultas. Restrito inteiramente ao bloqueio lógico Oauth2 JWT exigindo escopos médicos (`patient/*.read`), viabilizando acesso unicamente com validação provada em barreiras institucionais.

---

## 🚀 Como Executar em Máquina Local

Para levantar todo esse mini hospital de telemetria na sua máquina local de desenvolvimento ou testes na faculdade, utilize nativamente o *Docker Compose*, que cuida de criar as redes de interconexão internas dinamicamente.

1. **Clone** este repositório:
   ```bash
   git clone https://github.com/SeuUsuario/tcc-hah-fhir-architecture.git
   cd tcc-hah-fhir-architecture
   ```
2. **Suba o Ecosistema Completo de Plataformas e Bots em Nuvem-Local**:
   ```bash
   docker-compose up --build -d
   ```
3. O status de roteamento em segundo plano levantará as pontes:
   - Interface Kafka UI (Painel das Fila de Envio Diário) na porta `http://localhost:8080/`
   - O Swagger/OpenAPI interacionista do Backend (FastAPI Endpoint) nas portas REST via `http://localhost:8000/docs/`.

---

## 🛡️ Autenticação Inteligente & API (Smart on FHIR Mock) 

O sistema não transita e nem emite retornos FHIR a clientes "Anonymous". As vias base (`/fhir/Observation`) exigem atrelamento Bearer.

Faça a requisição (Mock Setup) no endpoint `POST /auth/token` consumindo as credenciais:
- **Username**: `clinician`
- **Password**: `supersecure`

O token entregue trará os scopes garantidores que desbloquearão o GET nas consultas simuladas parametrizadas ao seu painel.

---

## ✅ Engenharia e Qualidade

O repositório é testado via Continuous Integration (CI) com instanciamento `Pytest` garantido sempre de bater nas lógicas de transformação e acesso FHIR restrito não corrompendo a tipia universal. Todos os resultados de testes de vazão (Throughput superior a 22k req. assíncrona) figuram resiliência à rede projetada.

*Projeto estrutural atrelado aos pilares das normas acadêmicas em Engenharia de Software da ESALQ/USP.*
