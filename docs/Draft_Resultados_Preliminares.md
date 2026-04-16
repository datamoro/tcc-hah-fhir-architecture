# DRAFT — Resultados e Discussão (Resultados Preliminares)

> **Instrução do template oficial (ESALQ/USP):**
> *"Nesta seção devem ser apresentados, discutidos e interpretados os resultados obtidos, ou seja, os autores devem fazer uma discussão comparativa dos resultados do seu trabalho com aqueles existentes na literatura científica. É necessário elaborar uma análise crítica dos dados, destacando as limitações e pontos positivos dos resultados apresentados e da metodologia utilizada."*
>
> **Nota de redação:** Este draft deve ser reescrito em **pretérito perfeito do indicativo** no formato impessoal antes da entrega.

---

## Resultados e Discussão

### 3.1 Implementação da Infraestrutura e Pipeline de Ingestão

A infraestrutura distribuída foi provisionada por meio de contêineres Docker, utilizando o arquivo `docker-compose.yml` para orquestrar os serviços de mensageria e persistência. O cluster Apache Kafka foi configurado com suporte ao ZooKeeper para coordenação de nós, e a interface Kafka UI foi disponibilizada na porta 8080 para monitoramento em tempo real dos tópicos e partições.

O componente de ingestão de dados foi implementado como um produtor Kafka em Python (`app/ingestion/producer.py`), responsável por simular o envio contínuo de sinais vitais de três pacientes distintos (P001, P002, P003) em intervalos de 1 segundo. Cada mensagem publicada no tópico `raw-sensor-data` contém os seguintes parâmetros fisiológicos: frequência cardíaca (FC), oximetria de pulso (SpO2), pressão arterial sistólica e diastólica. Os dados são serializados em formato JSON e publicados com timestamp em UTC, o que garante rastreabilidade temporal independente do fuso horário de origem.

A adoção do Apache Kafka como barramento de mensageria assíncrona está alinhada com os princípios de desacoplamento e resiliência descritos por Newman (2015), que argumenta que arquiteturas orientadas a eventos permitem que componentes críticos sejam escalados ou substituídos de forma independente — característica essencial em sistemas de monitoramento clínico contínuo.

---

### 3.2 Transformação Semântica para o Padrão HL7 FHIR

O componente de transformação (`app/transformation/worker.py`) foi implementado como um worker Kafka que consome mensagens do tópico `raw-sensor-data` e realiza o mapeamento semântico dos dados brutos para o padrão HL7 FHIR R4. Para cada registro de sinal vital recebido, é instanciado um recurso FHIR do tipo `Observation`, utilizando a biblioteca Python `fhir.resources`.

O mapeamento para frequência cardíaca foi implementado com código LOINC `8867-4` ("Heart rate"), unidade de medida `beats/minute` referenciada pelo sistema `http://unitsofmeasure.org`, e referência ao paciente no formato `Patient/{patient_id}`, em conformidade com as especificações de referência do padrão FHIR R4. O dispositivo de origem foi registrado no campo `device`, garantindo rastreabilidade da fonte de coleta.

Esta abordagem de transformação semântica é consistente com a metodologia utilizada em estudos recentes. Como demonstrado por Le et al. (2024), a integração do padrão FHIR com plataformas computacionais modernas permitiu a obtenção de tempos de resposta entre 50 ms e 300 ms em ambiente real, dentro dos padrões aceitáveis para sistemas clínicos. Os recursos FHIR gerados na presente implementação foram validados estruturalmente pela própria biblioteca `fhir.resources`, que aplica validação de esquema Pydantic V2, garantindo a integridade semântica dos objetos antes da persistência.

---

### 3.3 Persistência em Banco de Dados de Séries Temporais

O armazenamento dos recursos FHIR foi realizado no TimescaleDB, uma extensão do PostgreSQL otimizada para séries temporais. O modelo de dados adotado (`FHIRObservation`) utiliza uma abordagem híbrida, combinando colunas relacionais indexadas (patient_id, code, effective_datetime) com uma coluna JSONB que armazena o recurso FHIR completo. Essa estratégia permite tanto consultas analíticas eficientes por índices quanto a recuperação do objeto completo e padronizado.

A tabela `fhir_observations` foi convertida em uma *hypertable* do TimescaleDB, particionada automaticamente pela coluna `effective_datetime`. Esta conversão permite que o banco de dados gerencie de forma eficiente o crescimento contínuo de dados temporais, aplicando compressão nativa e paralelismo nas consultas por janela de tempo — funcionalidades essenciais para sistemas de monitoramento remoto que geram fluxo ininterrupto de dados fisiológicos.

---

### 3.4 Exposição dos Dados via API RESTful

A camada de exposição dos dados foi implementada utilizando o framework FastAPI (`app/api/main.py`), disponibilizando uma rota de consulta compatível com a especificação de pesquisa do FHIR: `GET /fhir/Observation`. A rota aceita os parâmetros `patient` e `code`, permitindo a filtragem por identificador de paciente (com suporte ao prefixo `Patient/` conforme a especificação FHIR) e por código LOINC de sinal vital.

A API retorna diretamente os objetos FHIR completos armazenados em formato JSONB, sem necessidade de remapeamento adicional, o que garante fidelidade ao padrão e latência mínima de resposta. A documentação interativa da API é gerada automaticamente pelo FastAPI via Swagger UI, reduzindo a barreira de adoção por desenvolvedores externos e alinhando-se ao objetivo de oferecer uma referência técnica open source replicável, conforme proposto nos resultados esperados do projeto de pesquisa.

---

### 3.5 Limitações Identificadas e Próximos Passos

A implementação atual representa um Produto Mínimo Viável (MVP) funcional do pipeline completo de ingestão, transformação e exposição de dados fisiológicos, com as seguintes limitações identificadas:

- **Cobertura de recursos FHIR**: O worker atual implementa apenas o mapeamento de frequência cardíaca (código LOINC 8867-4). Os mapeamentos para SpO2 (código 59408-5) e pressão arterial (código 55284-4) estão estruturados nos dados de ingestão, mas aguardam implementação no worker de transformação.
- **Autenticação e Segurança**: A API não implementa, neste estágio, mecanismos de autenticação (OAuth 2.0 / SMART on FHIR), previstos para a fase de validação final.
- **Dataset Clínico Real**: Os dados utilizados são sintéticos (simulados). A validação com dados reais do PhysioNet (MIMIC-IV) está prevista para as próximas etapas.
- **Testes de Carga**: Testes de estresse e latência com volume representativo ainda não foram executados.

Estas limitações não comprometem a demonstração da viabilidade arquitetural do modelo proposto, mas constituem os eixos prioritários das próximas etapas de desenvolvimento.

---

*[DRAFT — Rascunho para revisão e expansão. Reescrever em terceira pessoa, pretérito perfeito, conforme normas ESALQ/USP antes da entrega oficial.]*
