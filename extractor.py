# Author: Guilherme Crepaldi
"""
Extracao dos CSVs dos arquivos ZIP dos microdados do ENEM.
"""

import zipfile
from pathlib import Path

from config import EXTRACTED_DIR, CSV_ENCODING


def extrair_microdados(
    arquivo_zip: Path,
    ano: int,
    destino: Path = EXTRACTED_DIR,
) -> list[Path]:
    """
    Extrai os arquivos CSV de dentro do ZIP dos microdados.

    Args:
        arquivo_zip: Caminho para o arquivo .zip.
        ano: Ano dos dados (para organizar diretorio de saida).
        destino: Diretorio base para extracao.

    Returns:
        Lista de paths para os arquivos CSV extraidos.

    Raises:
        FileNotFoundError: Se o ZIP nao existir.
        zipfile.BadZipFile: Se o arquivo estiver corrompido.
    """
    if not arquivo_zip.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {arquivo_zip}")

    dir_ano = destino / str(ano)
    dir_ano.mkdir(parents=True, exist_ok=True)

    extraidos: list[Path] = []

    try:
        with zipfile.ZipFile(arquivo_zip, "r") as zf:
            # Lista todos os CSVs dentro do ZIP
            csv_members = [m for m in zf.namelist() if m.lower().endswith(".csv")]

            if not csv_members:
                print(f"[!] Nenhum CSV encontrado em {arquivo_zip.name}")
                return extraidos

            for member in csv_members:
                nome_arquivo = Path(member).name
                destino_csv = dir_ano / nome_arquivo

                with zf.open(member) as fonte:
                    conteudo = fonte.read()
                    with open(destino_csv, "wb") as f:
                        f.write(conteudo)

                extraidos.append(destino_csv)
                print(f"  [Extraido] {nome_arquivo} ({_tamanho_bytes(len(conteudo))})")

    except zipfile.BadZipFile as e:
        raise zipfile.BadZipFile(
            f"Arquivo corrompido ou invalido: {arquivo_zip.name}. "
            f"Tente baixar novamente. Erro: {e}"
        )

    return extraidos


def _tamanho_bytes(size: int) -> str:
    """Retorna tamanho em formato legivel."""
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}TB"
