# Projeto Executivo: Arquitetura Distribuída para Monitoramento Fisiológico no Modelo Hospital-at-Home

**Autor:** Caio Moro  
**Curso:** MBA em Engenharia de Software (USP)  
**Orientador:** Lucas José de Souza

---

## 1. Visão Geral do Projeto

Este projeto consiste no desenvolvimento e implementação de uma **arquitetura de software distribuída**, **orientada a eventos** e compatível com o padrão de interoperabilidade **HL7 FHIR**, destinada a suportar o modelo assistencial **Hospital-at-Home (HaH)**.

O objetivo principal é viabilizar o monitoramento contínuo de pacientes em domicílio através da ingestão, transformação e exposição eficiente de dados fisiológicos (sinais vitais), garantindo integridade, escalabilidade e interoperabilidade semântica.

## 2. Contextualização e Justificativa (Estudo Bibliográfico)

A pesquisa bibliográfica realizada aponta para uma transformação digital acelerada na saúde, impulsionada pela pandemia e pela necessidade de modelos de cuidado descentralizados (HaH).

*   **Interoperabilidade como Pilar:** Estudos (Lins et al., 2024; Vorisek et al., 2022) demonstram que sistemas isolados (silos) são o maior entrave para a saúde digital. O padrão **HL7 FHIR** se consolida como a solução definitiva para integração, permitindo troca de dados via APIs RESTful modernas.
*   **Avanços em HaH:** Artigos como "Barriers to hospital-at-home acceptance" e "Virtual Medicine Wards" reforçam que o sucesso do HaH depende de monitoramento confiável. O uso de **wearables** para detecção de anomalias cardíacas (Abutalip et al., 2024) gera um volume massivo de dados que arquiteturas monolíticas tradicionais não comportam.
*   **Arquitetura de Dados:** A adoção de bancos de dados de séries temporais e arquiteturas orientadas a eventos (Kafka) é citada como essencial para lidar com o fluxo contínuo de dados de sensores. A literatura (ex: "MIMIC-IV on FHIR") valida a conversão de datasets clínicos antigos para FHIR como forma de padronização.

## 3. Arquitetura da Solução

A solução será construída sob uma arquitetura de **Microsserviços Orientada a Eventos**, utilizando tecnologias Open Source robustas.

### 3.1. Componentes Principais

1.  **Fonte de Dados (Simulação):**
    *   Script consumidor de dados do **PhysioNet** (MIMIC-IV ou similar).
    *   Simula o envio contínuo de sinais vitais (FC, SpO2, PA) por dispositivos wearables.

2.  **Camada de Ingestão e Mensageria:**
    *   **Apache Kafka**: Responsável por receber o stream de dados brutos dos sensores. Garante desacoplamento e *backpressure*.

3.  **Motor de Transformação e Padronização:**
    *   **Worker Python**: Consome mensagens do Kafka.
    *   **Biblioteca `fhir.resources`**: Mapeia dados brutos para recursos FHIR R4/R5 (ex: `Observation`, `Patient`, `Device`).

4.  **Armazenamento (Persistência):**
    *   **TimescaleDB (PostgreSQL)**: Banco de dados relacional otimizado para séries temporais. Armazenará os recursos FHIR (em formato JSONB) indexados por tempo, permitindo consultas analíticas rápidas.

5.  **Camada de Exposição (API):**
    *   **FastAPI**: Interface RESTful moderna para disponibilizar os dados.
    *   Endpoints compatíveis com especificações FHIR (Search, Read).

### 3.2. Stack Tecnológico

*   **Linguagem:** Python 3.12+
*   **Orquestração:** Docker & Docker Compose
*   **Mensageria:** Apache Kafka (ou Redpanda para desenvolvimento leve)
*   **Database:** TimescaleDB
*   **API Framework:** FastAPI
*   **Bibliotecas Chave:** `fhir.resources`, `kafka-python`, `pydantic`, `sqlalchemy`.

## 4. Roteiro de Implementação (Roadmap)

O projeto será executado em 5 sprints principais:

### Fase 1: Fundação e Dados
*   [ ] Configuração do ambiente Docker (Kafka, TimescaleDB).
*   [ ] Seleção e download do dataset PhysioNet (amostra de sinais vitais).
*   [ ] Desenvolvimento do script "Simulador de Sensor".

### Fase 2: Pipeline de Ingestão
*   [ ] Criação dos tópicos Kafka (`raw-sensor-data`).
*   [ ] Implementação do Producer (envio de dados brutos).
*   [ ] Teste de throughput de ingestão.

### Fase 3: Core FHIR
*   [ ] Mapeamento de dados: Definição de perfis FHIR para Frequência Cardíaca e Oximetria.
*   [ ] Implementação do Consumer (Worker) de transformação.
*   [ ] Validação da conformidade dos objetos gerados com `fhir.resources`.

### Fase 4: Persistência e API
*   [ ] Modelagem do esquema no TimescaleDB (Tabelas híbridas: Relacional + JSONB).
*   [ ] Desenvolvimento da API FastAPI.
*   [ ] Implementação de rotas de consulta (ex: GET `/Observation?patient=123`).

### Fase 5: Validação e Documentação
*   [ ] Testes de carga (Stress testing).
*   [ ] Validação com validador oficial HL7 FHIR.
*   [ ] Documentação final e README.

## 5. Entregáveis

*   Repositório GitHub contendo todo o código fonte.
*   Arquivo `docker-compose.yml` para replicação imediata (“One-click run”).
*   Documentação técnica da arquitetura.
*   Relatório de validação de desempenho e conformidade.

---
*Este projeto executivo serve como guia mestre para o desenvolvimento do TCC/MVP, alinhado com a proposta aprovada e as melhores práticas da engenharia de software moderna.*
