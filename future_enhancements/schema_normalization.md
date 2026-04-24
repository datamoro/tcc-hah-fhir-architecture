# Feature: Schema Normalization & Vendor Mapping

## Contexto e Problema
Atualmente, o `worker.py` espera chaves rigidamente definidas (como `heart_rate`, `spo2`, `blood_pressure_systolic`) no payload JSON vindo do Kafka. No mundo real do monitoramento remoto (*Hospital-at-Home*), diferentes fabricantes de dispositivos (wearables) enviam dados usando nomenclaturas variadas (ex: `hrt-rate`, `HR`, `bpm`, `spo2_pct`).

Embora o sistema atual não quebre completamente (graças ao design em blocos isolados `try...except`), ele descarta a métrica se a chave for desconhecida. 

## Solução Proposta para Etapas Futuras
Implementar uma camada de "Mapeamento e Normalização de Schema" antes da criação do recurso FHIR. Essa camada funcionará como um tradutor, convertendo os payloads heterogêneos de múltiplos fornecedores em um único schema padrão (*Canonical Model*) que o worker já conhece.

### Prova de Conceito (Draft de Implementação)

O código abaixo ilustra como essa normalização pode ser introduzida de forma simples e escalável:

```python
# future_enhancements/payload_normalizer.py

# Dicionário de sinônimos/mapeamento por fabricantes
VENDOR_SCHEMA_MAP = {
    "heart_rate": ["heart_rate", "hrt-rate", "HR", "bpm", "pulse"],
    "spo2": ["spo2", "oxygen_saturation", "SpO2%", "ox"],
    "blood_pressure_systolic": ["blood_pressure_systolic", "bp_sys", "systolic", "sys"],
    "blood_pressure_diastolic": ["blood_pressure_diastolic", "bp_dia", "diastolic", "dia"]
}

def normalize_payload(raw_payload: dict) -> dict:
    """
    Varre o payload cru do Kafka e normaliza as chaves para o formato esperado pelo worker.
    """
    normalized = {}
    
    # Preserva metadados essenciais
    normalized['patient_id'] = raw_payload.get('patient_id')
    normalized['timestamp'] = raw_payload.get('timestamp')
    normalized['device_id'] = raw_payload.get('device_id')

    # Busca valores baseados na tabela de sinônimos
    for canonical_key, synonyms in VENDOR_SCHEMA_MAP.items():
        for synonym in synonyms:
            if synonym in raw_payload:
                normalized[canonical_key] = raw_payload[synonym]
                break # Encontrou o valor, move para o próximo sinal vital
                
    return normalized
```

### Como seria integrado ao `worker.py`

No loop de consumo de mensagens (`run_worker`), a integração seria minimalista:

```python
# Trecho do worker.py (modificado)
raw_data = json.loads(msg.value().decode('utf-8'))

# 1. Normalização do payload de múltiplos fornecedores
normalized_data = normalize_payload(raw_data)

# 2. Transformação para FHIR (agora com schema garantido)
hr_obs = create_heart_rate_observation(normalized_data)
# ...
```

## Benefícios Arquiteturais
1. **Escalabilidade de Fabricantes (Onboarding):** Quando o hospital comprar relógios de uma nova marca, basta adicionar os sinônimos da marca no `VENDOR_SCHEMA_MAP` sem reescrever a complexa lógica FHIR.
2. **Resiliência a Falhas:** Previne a perda de dados clínicos causada por inconsistências de firmware dos dispositivos.
3. **Desacoplamento Rigoroso:** O conversor FHIR fica totalmente agnóstico de hardware. Ele conhece apenas a estrutura canônica de entrada.
