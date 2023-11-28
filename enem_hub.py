#!/usr/bin/env python3
# Author: Guilherme Crepaldi
"""
ENEM Data Hub — CLI para baixar, extrair, limpar e amostrar
microdados do ENEM.

Uso:
    python enem_hub.py --ano 2023 2024 --baixar --limpar --amostra 10000
    python enem_hub.py --ano 2023 --baixar --extrair
    python enem_hub.py --ano 2024 --limpar --amostra 5000
    python enem_hub.py --list-years
"""

import argparse
import sys
from pathlib import Path

from config import ANOS_SUPORTADOS


def main():
    parser = argparse.ArgumentParser(
        description="ENEM Data Hub — Ferramenta para microdados do ENEM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python enem_hub.py --ano 2023 2024 --baixar --limpar --amostra 10000
  python enem_hub.py --ano 2023 --baixar --extrair
  python enem_hub.py --list-years
        """,
    )

    parser.add_argument(
        "--ano",
        type=int,
        nargs="+",
        help="Ano(s) para processar (ex: 2023 2024)."
        f" Suportados: {min(ANOS_SUPORTADOS)}-{max(ANOS_SUPORTADOS)}",
    )
    parser.add_argument(
        "--baixar",
        action="store_true",
        help="Baixa os arquivos ZIP do site do INEP",
    )
    parser.add_argument(
        "--extrair",
        action="store_true",
        help="Extrai CSVs dos ZIPs baixados",
    )
    parser.add_argument(
        "--limpar",
        action="store_true",
        help="Limpa os dados: remove colunas inuteis, padroniza tipos",
    )
    parser.add_argument(
        "--amostra",
        type=int,
        nargs="?",
        const=10000,
        default=None,
        metavar="N",
        help="Cria amostra com N linhas (default: 10000 se usado sem valor)",
    )
    parser.add_argument(
        "--list-years",
        action="store_true",
        help="Lista os anos suportados e sai",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        dest="todos_anos",
        help="Processa todos os anos suportados (2009-2025)",
    )

    args = parser.parse_args()

    # ── Flag especial: listar anos ───────────────────────────────────────
    if args.list_years:
        print("Anos suportados pelo ENEM Data Hub:")
        for ano in ANOS_SUPORTADOS:
            print(f"  • {ano}")
        print(f"\nTotal: {len(ANOS_SUPORTADOS)} anos")
        sys.exit(0)

    # ── Validar anos ─────────────────────────────────────────────────────
    anos = []
    if args.todos_anos:
        anos = list(ANOS_SUPORTADOS)
        print(f"[Info] Processando todos os {len(anos)} anos disponiveis")
    elif args.ano:
        for a in args.ano:
            if a not in ANOS_SUPORTADOS:
                print(f"[!] Ano {a} nao esta na lista de suportados "
                      f"({min(ANOS_SUPORTADOS)}-{max(ANOS_SUPORTADOS)})")
                sys.exit(1)
        anos = args.ano
    else:
        parser.print_help()
        print("\n[!] Informe ao menos um ano (--ano) ou --all ou --list-years")
        sys.exit(1)

    if not (args.baixar or args.extrair or args.limpar or args.amostra is not None):
        print("[!] Nenhuma acao especificada. Use --baixar, --extrair, --limpar e/ou --amostra")
        sys.exit(1)

    # ── Pipeline ─────────────────────────────────────────────────────────
    from config import RAW_DIR, EXTRACTED_DIR, CLEAN_DIR, SAMPLES_DIR

    zips_baixados: dict[int, Path] = {}
    csvs_extraidos: dict[int, list[Path]] = {}
    csvs_limpos: dict[int, Path] = {}

    # 1) BAIXAR
    if args.baixar:
        from downloader import baixar_microdados

        print("\n" + "=" * 60)
        print("  ETAPA 1: Download dos ZIPs")
        print("=" * 60)
        for ano in anos:
            try:
                zips_baixados[ano] = baixar_microdados(ano, RAW_DIR)
            except Exception as e:
                print(f"[Erro] Falha ao baixar ENEM {ano}: {e}")

    # 2) EXTRAIR
    if args.extrair:
        from extractor import extrair_microdados

        print("\n" + "=" * 60)
        print("  ETAPA 2: Extracao dos CSVs")
        print("=" * 60)
        for ano in anos:
            zip_path = zips_baixados.get(ano) or (RAW_DIR / f"microdados_enem_{ano}.zip")
            if not zip_path.exists():
                print(f"[!] ZIP de {ano} nao encontrado. Use --baixar primeiro.")
                continue
            try:
                csvs = extrair_microdados(zip_path, ano, EXTRACTED_DIR)
                if csvs:
                    csvs_extraidos[ano] = csvs
            except Exception as e:
                print(f"[Erro] Falha ao extrair ENEM {ano}: {e}")

    # 3) LIMPAR
    if args.limpar:
        from cleaner import limpar_todos_anos

        print("\n" + "=" * 60)
        print("  ETAPA 3: Limpeza dos dados")
        print("=" * 60)
        csvs_limpos = limpar_todos_anos(anos)

    # 4) AMOSTRA
    if args.amostra is not None:
        from sampler import criar_amostra

        print("\n" + "=" * 60)
        print(f"  ETAPA 4: Criacao de amostra ({args.amostra} linhas)")
        print("=" * 60)

        # Tenta usar CSVs limpos primeiro, depois extraidos
        for ano in anos:
            caminho_fonte = csvs_limpos.get(ano)

            if caminho_fonte is None:
                # Procura no diretorio de extraidos
                dir_ano = EXTRACTED_DIR / str(ano)
                if dir_ano.exists():
                    csvs = list(dir_ano.glob("*_limpo.csv")) or list(dir_ano.glob("*.csv"))
                    if csvs:
                        caminho_fonte = csvs[0]

            if caminho_fonte and caminho_fonte.exists():
                try:
                    criar_amostra(caminho_fonte, ano, args.amostra, SAMPLES_DIR)
                except Exception as e:
                    print(f"[Erro] Falha ao criar amostra ENEM {ano}: {e}")
            else:
                print(f"[!] Nenhum dado encontrado para {ano}. Pule --amostra ou processe antes.")

    print("\n" + "=" * 60)
    print("  Concluido!")
    print("=" * 60)


if __name__ == "__main__":
    main()
