# ENEM Data Hub

A modular Python toolkit for downloading, extracting, cleaning, and sampling microdata from the Brazilian **ENEM** (Exame Nacional do Ensino Médio) exams, published by **INEP**.

## Features

- **Download** — Fetch ZIP files directly from INEP's official servers with progress bars and automatic retries
- **Extract** — Unpack CSV files from ZIP archives, handling INEP's standard encoding and separators
- **Clean** — Remove useless columns, standardize data types, and handle missing values
- **Sample** — Create reduced datasets for fast testing and development
- **CLI** — Single entry point to orchestrate the full pipeline

## Installation

```bash
git clone https://github.com/yourusername/enem-data-hub.git
cd enem-data-hub
pip install -r requirements.txt
```

## Usage

### Download microdata for specific years

```bash
python enem_hub.py --ano 2023 2024 --baixar
```

### Download, extract, clean, and create a sample

```bash
python enem_hub.py --ano 2023 --baixar --extrair --limpar --amostra 10000
```

### Process all available years at once

```bash
python enem_hub.py --all --baixar --extrair
```

### List supported years

```bash
python enem_hub.py --list-years
```

## Directory Structure

```
enem-data-hub/
├── enem_hub.py          # CLI entry point
├── downloader.py        # HTTP download with retry logic
├── extractor.py         # ZIP extraction for INEP microdata format
├── cleaner.py           # Data cleaning pipeline
├── sampler.py           # Random sampling for quick testing
├── models.py            # Data classes: Candidato, Escola, Notas
├── config.py            # URLs, paths, and configuration constants
├── requirements.txt     # Python dependencies
├── .gitignore
├── README.md
└── notas.md             # Personal development notes
```

## Data Format Notes

- INEP distributes microdata as ZIP files containing CSV files
- CSVs use `;` (semicolon) as separator and `latin1` encoding
- The CSV structure changed in **2020** — compatibility checks are in place
- INEP updates download URLs periodically; `config.py` centralizes URL management

## Supported Years

| Range | Status |
|-------|--------|
| 2009–2025 | Supported (configurable in `config.py`) |

## Requirements

- Python 3.10+
- requests, tqdm, pandas, numpy, colorama

## License

MIT

## Author

👤 **Author** — **Guilherme Crepaldi**
