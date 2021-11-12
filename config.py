# Author: Guilherme Crepaldi
"""
Configuracoes do ENEM Data Hub.
URLs, anos suportados, paths padronizados.
"""

from pathlib import Path

# ── Diretorios ──────────────────────────────────────────────────────────────
PROJETO_DIR = Path(__file__).parent.resolve()
DATA_DIR = PROJETO_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
EXTRACTED_DIR = DATA_DIR / "extracted"
CLEAN_DIR = DATA_DIR / "clean"
SAMPLES_DIR = DATA_DIR / "samples"

for _dir in [DATA_DIR, RAW_DIR, EXTRACTED_DIR, CLEAN_DIR, SAMPLES_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)

# ── Anos suportados ─────────────────────────────────────────────────────────
# INEP mudou o formato do CSV em 2020, precisa verificar compatibilidade
ANOS_SUPORTADOS = list(range(2009, 2026))  # 2009 ate 2025

# ── URLs base do INEP ───────────────────────────────────────────────────────
# INEP muda a URL todo ano, precisamos acompanhar
URL_BASE = "https://download.inep.gov.br/microdados"
URL_FORMAT = (
    "https://download.inep.gov.br"
    "/microdados"
    "/enem"
    "/microdados_enem_{ano}.zip"
)

# ── Nomes de arquivos conhecidos dentro dos ZIPs ────────────────────────────
# (variam conforme o ano, mas o padrao e 'DADOS' ou 'dados' no nome)
CSV_PATTERNS = [
    "DADOS/*.csv",
    "dados/*.csv",
    "**/*.csv",
]

# ── Encoding / separador ────────────────────────────────────────────────────
# CSV do ENEM vem com sep ; e encoding latin1. Padrao Brasil.
CSV_ENCODING = "latin1"
CSV_SEPARATOR = ";"

# ── Colunas consideradas inuteis para a maioria das analises ────────────────
COLUNAS_INUTEIS = [
    "TP_FICHA_1",       # nao lembro pra que serve essa coluna, vou dropar
    "TP_FICHA_2",
    "TP_FICHA_3",
    "TP_FICHA_4",
    "TP_FICHA_5",
    "TP_FICHA_6",
    "TP_FICHA_7",
    "TP_FICHA_8",
    "TP_FICHA_9",
    "TP_FICHA_10",
    "TP_FICHA_11",
    "TP_FICHA_12",
    "TP_FICHA_13",
    "TP_FICHA_14",
    "TP_FICHA_15",
    "TP_FICHA_16",
    "TP_FICHA_17",
    "TP_FICHA_18",
    "TP_FICHA_19",
    "TP_FICHA_20",
    "TP_FICHA_21",
    "TP_FICHA_22",
    "TP_FICHA_23",
    "TP_FICHA_24",
    "TP_FICHA_25",
    "TP_STATUS_REDACAO",
    "TP_LINGUA",
    "TP_PRESENCA_CN",
    "TP_PRESENCA_CH",
    "TP_PRESENCA_LC",
    "TP_PRESENCA_MT",
]

# ── Colunas de nota (para calcular media) ───────────────────────────────────
COLUNAS_NOTAS = [
    "NU_NOTA_CN",
    "NU_NOTA_CH",
    "NU_NOTA_LC",
    "NU_NOTA_MT",
    "NU_NOTA_REDACAO",
]

# ── Config de download ──────────────────────────────────────────────────────
TIMEOUT = 60  # segundos
MAX_RETRIES = 3
RETRY_DELAY = 5  # segundos entre tentativas
