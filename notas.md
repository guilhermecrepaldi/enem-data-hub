# Anotacoes pessoais — ENEM Data Hub

## Por que esse projeto?

Surgiu da necessidade de ter uma ferramenta confiavel pra baixar e tratar
os microdados do ENEM sem depender de scripts jogados fora.
O INEP disponibiliza os dados mas o formato muda quase todo ano,
entao ter um pipeline padronizado economiza horas.

## Problemas conhecidos

- **URL do INEP muda direto.** Ja tive que atualizar a URL_BASE umas 3 vezes.
  A estrutura do site do INEP nao e estavel.
- **CSV de 2020 mudou o formato.** Colunas novas, algumas removidas.
  Preciso verificar se o mapeamento atual cobre tudo.
- **Arquivos grandes.** Um CSV completo tem 1M+ linhas e ~500MB.
  A amostragem e essencial pra nao travar o PC.
- **Encoding latin1 vs utf-8.** O INEP ainda usa latin1 nos CSVs.
  Ja processei convertendo pra utf-8-sig na saida pra evitar BOM.

## Ideias futuras

- [ ] Adicionar suporte a download paralelo (asyncio?) pra varios anos
- [ ] Exportar direto pra Parquet (mais rapido que CSV)
- [ ] Criar analises basicas automaticas (medias por ano, escola, regiao)
- [ ] Dashboard simples com Streamlit
- [ ] Cache de metadados pra nao reprocessar o mesmo CSV
- [ ] Testes unitarios com pytest (usando as amostras)

## Comandos uteis (debug)

```bash
# Ver estrutura de um CSV sem carregar tudo
head -1 data/raw/microdados_enem_2023.zip | python -c "
import zipfile, sys
with zipfile.ZipFile(sys.stdin.read().strip()) as z:
    print(z.namelist())
"

# Contar linhas de um CSV
wc -l data/extracted/2023/DADOS_ENEM_2023.csv

# Amostra rapida via shell (sem o sampler)
head -1 arquivo.csv > amostra.csv
shuf -n 1000 arquivo.csv >> amostra.csv
```

## Contato

Dev real brasileiro. Qualquer duvida so chamar.

## Autor

**Guilherme Crepaldi**
