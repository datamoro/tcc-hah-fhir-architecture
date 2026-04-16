# Pauta da Reunião de Orientação - TCC Caio Moro

**Data:** [Preencher Data]  
**Participantes:** Caio Moro (Orientando), Prof. Lucas José de Souza (Orientador)

## 1. Alinhamento de Expectativas e Prazos
- **Status do Cronograma**: Breve menção ao atraso e confirmação do termo de prorrogação assinado.
- **Compromisso com o Template**: Confirmação de que a migração para o template oficial da ESALQ/USP já está em andamento (meta: conclusão em 48h).

## 2. Apresentação do Progresso Técnico (O "MVP")
- **Arquitetura Implementada**:
    - Pipeline de dados funcionando em Docker.
    - Simulação de sensores (Ingestão via Kafka).
    - Transformação semântica para o padrão **HL7 FHIR** (uso da biblioteca `fhir.resources`).
    - Persistência em banco de séries temporais (**TimescaleDB**).
    - Camada de API (**FastAPI**) para consulta dos recursos FHIR.
- **Demonstração Rápida**: [Opcional] Mostrar o container rodando e a primeira rota da API funcionando.

## 3. Metodologia de Validação
- **Base de Dados**: Uso planejado do dataset **PhysioNet** para validar o mapeamento FHIR com dados clínicos reais.
- **Conformidade**: Uso de validadores oficiais FHIR para garantir a qualidade do framework.

## 4. Dúvidas e Feedback para o Orientador
- Prof., o enfoque no "Framework Open Source" (ao invés de apenas um sistema final) é a principal contribuição para o MBA?
- O uso de datasets simulados (como PhysioNet) é aceitável para a "entrega de resultados preliminares" ou você espera testes com dispositivos reais?

## 5. Próximos Passos (Acordados)
- [ ] Submissão do arquivo no template oficial via plataforma.
- [ ] Reenvio/Ajuste dos "resultados preliminares".
- [ ] Próxima data de entrega.
