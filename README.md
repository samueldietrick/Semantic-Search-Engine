<p align="center">
  <img src="img.png" alt="Semantic Search Engine" width="720" />
</p>

# Semantic Search Engine

Busca em linguagem natural sobre um índice vetorial no [Qdrant](https://qdrant.tech/), com ranking misto: similaridade de embeddings (`sentence-transformers`) mais um componente lexical (tokens, peso por campo, fuzzy). A API é FastAPI; o front é React com Vite e Tailwind.

O fluxo é: você sobe o Qdrant, indexa JSON (ou JSONL) com o script em `indexer/`, sobe a API e opcionalmente o front para testar no navegador.

## O que tem no repositório

- **`indexer/`** — lê dados, gera vetores, grava no Qdrant. Suporta alias de coleção (útil para trocar versão sem mudar o nome que a API usa).
- **`api/`** — `POST /search` com score final, scores separados, highlights e textos explicando o match.
- **`frontend/`** — interface de busca; em dev o Vite encaminha `/search` para a API local.
- **`data/`** — exemplo `sample.json` (gerado por `scripts/generate_sample.py` se quiser recriar).
- **`shared/`** — normalização de texto e stopwords usados no lado lexical da API.

## Pré-requisitos

- Python 3.10 ou superior
- Node.js 18+ (só para o front)
- Docker (recomendado para rodar o Qdrant sem instalar à parte)

Na primeira execução o modelo `paraphrase-multilingual-MiniLM-L12-v2` é baixado do Hugging Face; pode levar alguns minutos dependendo da rede.

## Qdrant

Na raiz do clone:

```bash
docker compose up -d
```

Serviço HTTP em `http://localhost:6333`. Para parar: `docker compose down`.

Se preferir Qdrant instalado por outro meio, só aponte a URL nas variáveis abaixo.

## Dependências Python

Com venv ativado, na raiz:

```bash
pip install -r requirements.txt
```

Isso puxa `indexer/requirements.txt` e `api/requirements.txt`. Se quiser instalar só uma parte, use esses arquivos separadamente.

## Indexar dados

Gere o JSON de exemplo (opcional, já existe em `data/sample.json`):

```bash
python scripts/generate_sample.py
```

Indexação na coleção física `items_v1` e alias `items` (é esse nome que a API usa por padrão):

```bash
python -m indexer.cli --data data/sample.json --collection items_v1 --alias items
```

Parâmetros úteis:

- `--qdrant-url` — padrão `http://localhost:6333`
- `--model` — mesmo modelo que a API (`EMBEDDING_MODEL`); default é `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- `--batch-size` — tamanho do lote de embeddings (default 64)

Para reindexar sem derrubar quem lê pelo nome estável: crie outra coleção (`items_v2`), indexe nela e rode de novo com `--alias items`. O alias passa a apontar para a coleção nova.

Arquivos muito grandes: use **JSONL** (uma linha JSON por documento) e extensão `.jsonl`; o indexador lê em streaming. Lotes grandes ajudam na throughput, não na memória do arquivo em si.

### Formato dos documentos

Cada objeto precisa de um `id` estável. O resto é flexível: por exemplo `titulo`, `descricao`, `tags`, `metadata`. O texto que vai para o embedding é montado a partir desses campos (detalhe em `indexer/stream_loader.py`).

### IDs e Qdrant

O servidor REST do Qdrant aceita só **inteiro sem sinal** ou **UUID** como id do ponto. O seu `id` de negócio (ex.: `item:42`) continua no **payload** e é o que volta na API. No indexador, strings que não são só dígitos viram um **UUID v5** determinístico; só dígitos viram inteiro. Veja `indexer/point_ids.py`.

## API

A pasta `api/` precisa ver o pacote `app` e o diretório raiz (módulo `shared`). No Linux/macOS, a partir da raiz do repositório:

```bash
export PYTHONPATH="$(pwd):$(pwd)/api"
cd api
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

No PowerShell (Windows), na raiz:

```powershell
$env:PYTHONPATH = "$PWD;$PWD\api"
cd api
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Copie `api/.env.example` para `api/.env` e ajuste se precisar. Principais variáveis:

- `QDRANT_URL` — default `http://localhost:6333`
- `COLLECTION_NAME` — default `items` (use o **alias** criado na indexação)
- `SEMANTIC_WEIGHT` / `LEXICAL_WEIGHT` — default `0.7` e `0.3`
- `QDRANT_PREFETCH` — quantos vizinhos vetoriais buscar antes de reranquear
- `CACHE_TTL_SECONDS` — cache de resposta para a mesma query (só primeira página)

Endpoints:

- `GET /health`
- `POST /search` — corpo JSON: `{"q": "...", "limit": 10, "offset": 0}`

Exemplo com curl (Linux/macOS/Git Bash):

```bash
curl -s -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"q": "curso de backend barato", "limit": 5}'
```

No `cmd.exe` do Windows as aspas e o `^` para quebra de linha são diferentes; o mais simples é uma linha só ou usar PowerShell `Invoke-RestMethod`.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Abra `http://localhost:5173`. Com a API na porta 8000, o proxy do Vite já encaminha as requisições.

Build de produção (gera `frontend/dist`):

```bash
npm run build
```

Para apontar para uma API em outro host, crie `frontend/.env`:

```
VITE_API_URL=http://seu-host:8000
```

(Sem barra no final.)

## Testes

Na raiz, com o mesmo `PYTHONPATH` da API:

```bash
python -m pytest api/tests -v
```

## Como o ranking funciona (resumo)

Primeiro o Qdrant devolve os vizinhos mais próximos no espaço de embeddings; os scores são normalizados no lote. Em seguida calcula-se um score lexical sobre título, descrição, tags e metadata (com pesos diferentes) e fuzzy onde não há match direto. O score final é a combinação linear dos dois, com pesos configuráveis. Os "motivos" e highlights vêm dessa análise.

## Licença

Defina a licença no seu fork (MIT, Apache-2.0, etc.) conforme a política do repositório.
