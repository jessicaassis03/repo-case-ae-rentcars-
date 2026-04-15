#  Rentcars | Case Técnico — Senior Analytics Engineer

## 🎯 Objetivo

Construir uma solução analítica completa a partir de dados brutos com problemas intencionais de qualidade, transformando-os em **informação confiável para tomada de decisão**.

---

## 🏗️ Arquitetura de Dados

```
RAW → STAGING → INTERMEDIATE → MARTS → ANALYTICS
```

* **Staging:** limpeza, padronização e deduplicação
* **Intermediate:** aplicação de regras de negócio
* **Marts:** modelo analítico (Star Schema)

---

##  Modelagem

### Dimensões

* `dim_users`
* `dim_partners`

### Fatos

* `fct_sessions`
* `fct_bookings`

---

##  Qualidade de Dados

Foram tratados:

* Duplicatas (ROW_NUMBER)
* Inconsistência de case (UPPER/LOWER)
* Bots (`is_bot = true`)
* Datas inválidas
* Valores negativos e outliers
* Relacionamentos inválidos

---

##  Principais Insights

* Alta taxa de cancelamento reduz receita líquida
* Bots impactam negativamente o funil
* Conversão varia por device
* Volume de busca não garante conversão

---

##  Governança

* SLA definido
* Catálogo de métricas
* Data contracts
* Tratamento de PII

---

##  Execução

```bash
dbt seed
dbt run
dbt test
```

---

## ⚠️ Assunções

* Receita considera apenas bookings `confirmed` e `completed`
* Bots são excluídos de análises
* Cancelamentos impactam receita líquida

---

##  Diferenciais

* Modelos incrementais
* Testes customizados
* Detecção de fraude
* Discovery com stakeholders

---

## 📂 Documentação

* `docs/data_dictionary.md`
* `governance.md`
* `stakeholders/`
