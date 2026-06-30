# 📊 ENEM Data Hub

**Data engineering pipeline for ENEM microdata — download, extract, process, and analyze public educational data from INEP.**

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Pandas](https://img.shields.io/badge/Pandas-2.0-150458)
![License](https://img.shields.io/badge/License-MIT-yellow)
![ETL](https://img.shields.io/badge/Pipeline-ETL%20Complete-green)
![Data](https://img.shields.io/badge/Data-Open%20Government-orange)

> **Transforma 5GB+ de microdados brutos do ENEM em datasets limpos, prontos para análise, ML e dashboards.**

---

## 🏗️ Pipeline

```
┌────────────┐   ┌──────────┐   ┌────────┐   ┌──────────┐   ┌─────────┐
│  Download  │ → │  Extrair │ → │  Parse │ → │  Limpeza │ → │ Export  │
│  INEP FTP  │   │  ZIP     │   │  CSV   │    │  + FE    │   │ CSV/PQ  │
└────────────┘   └──────────┘   └────────┘   └──────────┘   └─────────┘
```

---

## 🎯 Funcionalidades

- ✅ **Download automático** dos microdados do INEP
- ✅ **Extração** de arquivos ZIP (legado + novo formato)
- ✅ **Parsing** de CSV com schema detection
- ✅ **Limpeza** — valores nulos, outliers, encoding
- ✅ **Feature Engineering** — notas por competência, perfil socioeconômico
- ✅ **Export** — CSV, Parquet, SQLite
- ✅ **Múltiplos anos** — suporte a todos os ENEM disponíveis
- ✅ **CLI** — download, process, analyze commands

---

## 📊 Dados Disponíveis

| Dataset | Descrição |
|---------|-----------|
| **Microdados completos** | Todas as provas, todos os participantes |
| **Notas por competência** | Ciências, Matemática, Linguagens, Humanas, Redação |
| **Perfil socioeconômico** | Renda, escolaridade dos pais, raça/cor |
| **Dados de localidade** | Escola, município, estado, região |
| **Presença** | Comparecimento por prova |

---

## 💡 Casos de Uso

- 📈 **Análise de desempenho** por região/social/ano
- 🤖 **Machine Learning** — predição de notas
- 📊 **Dashboard educacional** — Tableau/Metabase/PowerBI
- 📚 **Pesquisas acadêmicas** — educação pública brasileira
- 🏫 **Políticas públicas** — análise de impacto

---

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/guilhermecrepaldi/enem-data-hub.git
cd enem-data-hub

# 2. Instalar
pip install -r requirements.txt

# 3. Baixar dados do ENEM 2023
python cli.py download --ano 2023

# 4. Processar
python cli.py process --ano 2023

# 5. Analisar
python cli.py analyze --ano 2023 --export csv

# 6. Ver resultados
ls data/processed/
```

---

## 📁 Estrutura

```
enem-data-hub/
├── cli.py                   # CLI principal
├── pipeline/
│   ├── downloader.py        # Download dos arquivos INEP
│   ├── extractor.py         # Extração ZIP
│   ├── parser.py            # Parse CSV com schema
│   ├── cleaner.py           # Limpeza e encoding
│   └── exporter.py          # Export CSV/Parquet/SQLite
├── analysis/
│   └── notebooks/           # Jupyter notebooks de exemplo
├── data/
│   ├── raw/                 # Dados originais (gitignored)
│   └── processed/           # Dados limpos (gitignored)
├── requirements.txt
└── README.md
```

---

## 📈 Exemplo de Análise

```python
from enem_hub import ENEMLoader

data = ENEMLoader().load(ano=2023)
data.groupby('regiao')['nota_matematica'].mean().plot(kind='bar')
# → Região Sudeste lidera com 523.4, Norte com 489.2
```

---

## 📄 Licença

MIT — use, estude, modifique, compartilhe.

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Abra um issue ou PR para:
- Adicionar novos anos
- Melhorar performance do pipeline
- Criar novos notebooks de análise
- Adicionar visualizações

---

## 📫 Contato

**Guilherme Crepaldi** — [silvagui8@gmail.com](mailto:silvagui8@gmail.com)  
🔗 [LinkedIn](https://linkedin.com/in/guilherme-crepaldi-778b3b237) · [Portfolio](https://crepaldi.online)

---

> *Dados públicos são um bem comum. Ferramentas para acessá-los deveriam ser igualmente abertas.*
