#  Governança e Qualidade de Dados

## 📌 Problemas Identificados

### Dados inconsistentes

* Países com múltiplos formatos (BR, Brazil)
* Campos nulos em colunas críticas

### Problemas estruturais

* Duplicatas em bookings e sessões
* Cancelamentos sem referência válida

### Problemas temporais

* Datas no futuro
* Sequência lógica inválida (cancelamento antes da reserva)

### Fraude / comportamento suspeito

* Sessões com mais de 50 buscas em poucos minutos

---

##  Regras de Validação

* `not_null` em chaves primárias
* `unique` para evitar duplicidade
* `relationships` entre fatos e dimensões
* Testes customizados para datas inválidas

---

## 📊 SLA de Dados

| Métrica      | Threshold |
| ------------ | --------- |
| Freshness    | < 2 horas |
| Completeness | > 99%     |
| Accuracy     | > 98%     |

---

##  PII

### Campos sensíveis

* user_id
* possíveis identificadores indiretos

### Estratégias

* Hash (SHA256)
* Anonimização
* Restrição de acesso

---

##  Catálogo de Métricas

### Receita Bruta

Total de bookings confirmados

### Receita Líquida

Receita bruta - cancelamentos

### Taxa de Conversão

bookings / sessões

---

##  Conclusão

A governança garante que os dados sejam:

* Confiáveis
* Auditáveis
* Alinhados com o negócio
