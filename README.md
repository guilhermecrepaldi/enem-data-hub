# enem-data-hub

**Ferramenta para baixar, extrair e processar microdados do ENEM (INEP)** — pipeline ETL completo para dados educacionais brasileiros.

## 🎯 Objetivo

Disponibilizar dados do ENEM de forma limpa, estruturada e pronta para análise — desde o download dos arquivos originais do INEP até datasets prontos para consumo.

## 🔧 Stack

- **Python** — pandas, requests, zipfile
- **ETL Pipeline** — extract → transform → load
- **Output** — CSV, Parquet, SQLite

## 🚀 Pipeline

```
Download INEP → Extração ZIP → Parse CSV → Limpeza → Feature Engineering → Export
```

## 📊 Dados Disponíveis

- Microdados completos por ano
- Notas por competência
- Perfil socioeconômico
- Dados de localidade (escola, município)

## 💡 Casos de Uso

- Análise de desempenho por região
- Machine Learning — predição de notas
- Dashboard educacional
- Pesquisas acadêmicas

---

> Projeto open source. Contribuições bem-vindas.
