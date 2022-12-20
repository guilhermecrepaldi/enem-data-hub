# Author: Guilherme Crepaldi
"""
Limpeza basica dos dados do ENEM.
Remove colunas inuteis, padroniza tipos, trata valores ausentes.
Funcoes que cresceram organicamente com o tempo.
"""

from pathlib import Path

import pandas as pd

from config import (
    CSV_ENCODING,
    CSV_SEPARATOR,
    COLUNAS_INUTEIS,
    COLUNAS_NOTAS,
    CLEAN_DIR,
    EXTRACTED_DIR,
)


def remover_colunas_inuteis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove colunas que nao sao uteis para analise.

    Algumas colunas como TP_FICHA_* sao misteriosas —
    nao lembro pra que serve essa coluna, vou dropar.
    """
    colunas_existentes = [c for c in COLUNAS_INUTEIS if c in df.columns]
    if colunas_existentes:
        print(f"  [Clean] Removendo {len(colunas_existentes)} colunas inuteis")
        return df.drop(columns=colunas_existentes)
    return df


def padronizar_tipos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converte colunas de nota para float e trata outros tipos.

    INEP muda os tipos de volta pra string as vezes...
    """
    for col in df.columns:
        # Converte colunas de nota para numero
        if col.startswith("NU_NOTA_") or col.startswith("NOTA_"):
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Converte colunas de presenca para categorias
        if col.startswith("TP_PRESENCA_"):
            df[col] = df[col].astype("Int64")

        # Colunas de prova (tipo de prova)
        if col.startswith("TP_PROVA_"):
            df[col] = df[col].astype("Int64")

    return df


def tratar_ausentes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trata valores ausentes de forma simples:
    - Notas NaN viram None
    - Colunas categoricas com -1 viram None (ausente por omissao)
    """
    # Colunas de nota: NaN permanece NaN (representa ausente)
    for col in COLUNAS_NOTAS:
        if col in df.columns:
            df[col] = df[col].where(df[col].notna(), None)

    # Colunas categoricas: -1 geralmente significa 'nao informado'
    for col in df.select_dtypes(include=["int", "Int64"]).columns:
        df[col] = df[col].replace(-1, pd.NA)

    return df


def limpar_microdados(
    caminho_csv: Path,
    ano: int,
    destino: Path = CLEAN_DIR,
) -> Path:
    """
    Pipeline completo de limpeza de um CSV do ENEM.

    Args:
        caminho_csv: Path para o CSV bruto.
        ano: Ano dos dados.
        destino: Diretorio de saida.

    Returns:
        Path para o CSV limpo.
    """
    print(f"\n[Limpeza] ENEM {ano} — {caminho_csv.name}")

    # CSV do ENEM vem com sep ; e encoding latin1. Padrao Brasil.
    df = pd.read_csv(
        caminho_csv,
        sep=CSV_SEPARATOR,
        encoding=CSV_ENCODING,
        low_memory=False,
    )
    print(f"  [OK] Carregado: {len(df)} linhas, {len(df.columns)} colunas")

    df = remover_colunas_inuteis(df)
    df = padronizar_tipos(df)
    df = tratar_ausentes(df)

    dir_ano = destino / str(ano)
    dir_ano.mkdir(parents=True, exist_ok=True)

    nome_limpo = f"enem_{ano}_limpo.csv"
    saida = dir_ano / nome_limpo

    df.to_csv(saida, sep=CSV_SEPARATOR, index=False, encoding="utf-8-sig")
    print(f"  [OK] Salvo: {saida.name} ({len(df)} linhas, {len(df.columns)} colunas)")

    return saida


def limpar_todos_anos(anos: list[int]) -> dict[int, Path]:
    """
    Limpa CSVs de varios anos.

    Args:
        anos: Lista de anos para processar.

    Returns:
        Dict {ano: path_do_csv_limpo}.
    """
    resultados = {}
    for ano in anos:
        dir_ano = EXTRACTED_DIR / str(ano)
        if not dir_ano.exists():
            print(f"[!] Diretorio de extracao nao encontrado para {ano}")
            continue

        csvs = list(dir_ano.glob("*.csv"))
        if not csvs:
            print(f"[!] Nenhum CSV encontrado em {dir_ano}")
            continue

        # Pega o maior CSV (geralmente o principal com os microdados)
        csv_principal = max(csvs, key=lambda p: p.stat().st_size)
        resultados[ano] = limpar_microdados(csv_principal, ano)

    return resultados
