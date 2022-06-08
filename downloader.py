# Author: Guilherme Crepaldi
"""
Download dos microdados do ENEM do site do INEP.
Baixa os ZIPs com barra de progresso e retry basico.
"""

import time
from pathlib import Path

import requests
from tqdm import tqdm

from config import (
    RAW_DIR,
    URL_FORMAT,
    TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY,
)


def baixar_microdados(
    ano: int,
    destino: Path = RAW_DIR,
    timeout: int = TIMEOUT,
) -> Path:
    """
    Baixa o ZIP de microdados do ENEM para um ano especifico.

    Args:
        ano: Ano desejado (ex: 2023).
        destino: Diretorio onde salvar o arquivo.
        timeout: Timeout da requisicao em segundos.

    Returns:
        Path para o arquivo ZIP baixado.

    Raises:
        ValueError: Se o download falhar apos MAX_RETRIES tentativas.
        requests.HTTPError: Se o servidor retornar erro 4xx/5xx.
    """
    # INEP muda a URL todo ano, precisamos acompanhar
    url = URL_FORMAT.format(ano=ano)
    arquivo_zip = destino / f"microdados_enem_{ano}.zip"

    if arquivo_zip.exists():
        print(f"[OK] Arquivo ja existe: {arquivo_zip.name} ({_tamanho(arquivo_zip)})")
        return arquivo_zip

    destino.mkdir(parents=True, exist_ok=True)

    ultimo_erro = None
    for tentativa in range(1, MAX_RETRIES + 1):
        try:
            print(f"[Download] ENEM {ano} — tentativa {tentativa}/{MAX_RETRIES}")
            print(f"  URL: {url}")

            resp = requests.get(url, stream=True, timeout=timeout)
            resp.raise_for_status()

            total_bytes = int(resp.headers.get("content-length", 0))
            desc = f"ENEM {ano}"
            with tqdm(
                total=total_bytes,
                unit="B",
                unit_scale=True,
                desc=desc,
                ncols=80,
            ) as pbar:
                with open(arquivo_zip, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                        pbar.update(len(chunk))

            print(f"[OK] {arquivo_zip.name} baixado ({_tamanho(arquivo_zip)})")
            return arquivo_zip

        except requests.RequestException as e:
            ultimo_erro = e
            print(f"  [!] Erro: {e}")
            if tentativa < MAX_RETRIES:
                print(f"  Aguardando {RETRY_DELAY}s antes de tentar novamente...")
                time.sleep(RETRY_DELAY)

    raise ValueError(
        f"Falha ao baixar ENEM {ano} apos {MAX_RETRIES} tentativas. "
        f"Ultimo erro: {ultimo_erro}"
    )


def _tamanho(path: Path) -> str:
    """Retorna tamanho do arquivo em formato legivel."""
    size = path.stat().st_size
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}TB"
