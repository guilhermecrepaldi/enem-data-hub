# Author: Guilherme Crepaldi
"""
Amostragem reduzida dos dados do ENEM para testes rapidos.

Cria versoes menores dos CSVs para desenvolvimento e debug
sem precisar carregar o dataset completo (~1M+ linhas).
"""

import pandas as pd

from pathlib import Path

from config import (
    CSV_ENCODING,
    CSV_SEPARATOR,
    SAMPLES_DIR,
)


def criar_amostra(
    caminho_csv: Path,
    ano: int,
    n_linhas: int = 10000,
    destino: Path = SAMPLES_DIR,
    seed: int = 42,
) -> Path:
    """
    Cria uma amostra aleatoria do CSV com N linhas.

    Args:
        caminho_csv: Path para o CSV completo.
        ano: Ano dos dados.
        n_linhas: Numero de linhas da amostra.
        destino: Diretorio de saida.
        seed: Semente aleatoria para reproducibilidade.

    Returns:
        Path para o CSV da amostra.

    Raises:
        FileNotFoundError: Se o arquivo fonte nao existir.
        ValueError: Se n_linhas <= 0.
    """
    if not caminho_csv.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {caminho_csv}")
    if n_linhas <= 0:
        raise ValueError(f"n_linhas deve ser positivo, recebido: {n_linhas}")

    print(f"\n[Amostra] ENEM {ano} — {n_linhas} linhas de {caminho_csv.name}")

    # Le apenas o cabecalho pra saber as colunas
    df_head = pd.read_csv(
        caminho_csv,
        sep=CSV_SEPARATOR,
        encoding=CSV_ENCODING,
        nrows=0,
    )

    # Conta linhas totais (rapido em arquivos grandes)
    total_linhas = sum(1 for _ in open(caminho_csv, "r", encoding=CSV_ENCODING)) - 1
    print(f"  Total de linhas no arquivo original: {total_linhas:,}")

    # Se pediu mais do que tem, usa tudo
    n_linhas = min(n_linhas, total_linhas)

    # Le o CSV pulando linhas aleatoriamente (amostragem sistemica)
    skip = sorted(
        set(range(1, total_linhas + 1)).difference(
            _sample_indices(total_linhas, n_linhas, seed)
        )
    )

    df = pd.read_csv(
        caminho_csv,
        sep=CSV_SEPARATOR,
        encoding=CSV_ENCODING,
        skiprows=skip,
        low_memory=False,
    )

    destino.mkdir(parents=True, exist_ok=True)
    nome_amostra = f"enem_{ano}_amostra_{n_linhas}.csv"
    saida = destino / nome_amostra

    df.to_csv(saida, sep=CSV_SEPARATOR, index=False, encoding="utf-8-sig")
    print(f"  [OK] Amostra salva: {saida.name} ({len(df)} linhas)")

    return saida


def _sample_indices(total: int, n: int, seed: int) -> set:
    """Gera indices aleatorios para amostragem."""
    import random
    rng = random.Random(seed)
    return set(rng.sample(range(1, total + 1), n))
