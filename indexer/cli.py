"""CLI do indexador: embeddings + Qdrant + alias opcional."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qdrant_client import QdrantClient
from qdrant_client.http import models as qm

from indexer.embedder import embed_texts
from indexer.qdrant_store import build_point, ensure_collection, set_alias, upsert_batch
from indexer.stream_loader import chunk_iterable, document_to_embedding_text, iter_json_items

DEFAULT_MODEL = os.environ.get(
    "EMBEDDING_MODEL",
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
)
DEFAULT_QDRANT = os.environ.get("QDRANT_URL", "http://localhost:6333")
DEFAULT_BATCH = 64


def main() -> None:
    p = argparse.ArgumentParser(description="Indexador semantico para Qdrant")
    p.add_argument("--data", type=Path, required=True, help="Arquivo JSON ou JSONL")
    p.add_argument(
        "--collection",
        type=str,
        required=True,
        help="Nome da coleção física (ex: items_v1)",
    )
    p.add_argument(
        "--alias",
        type=str,
        default=None,
        help="Alias estável apontando para esta coleção (ex: items)",
    )
    p.add_argument("--qdrant-url", type=str, default=DEFAULT_QDRANT)
    p.add_argument("--model", type=str, default=DEFAULT_MODEL)
    p.add_argument("--batch-size", type=int, default=DEFAULT_BATCH)
    args = p.parse_args()

    if not args.data.is_file():
        raise SystemExit(f"Arquivo não encontrado: {args.data}")

    client = QdrantClient(url=args.qdrant_url)
    probe = embed_texts(args.model, ["probe"], batch_size=1)
    dim = len(probe[0])
    ensure_collection(client, args.collection, vector_size=dim)

    iterator = iter_json_items(args.data)
    total = 0
    for batch in chunk_iterable(iterator, args.batch_size):
        texts = [document_to_embedding_text(d) for d in batch]
        vectors = embed_texts(args.model, texts, batch_size=len(texts))
        points: list[qm.PointStruct] = []
        for doc, vec in zip(batch, vectors, strict=True):
            if doc.get("id") is None:
                raise ValueError("Documento sem campo 'id'")
            payload = dict(doc)
            points.append(build_point(vec, payload))
        upsert_batch(client, args.collection, points)
        total += len(points)
        print(f"Indexados {total} pontos...", flush=True)

    if args.alias:
        set_alias(client, args.alias, args.collection)
        print(f"Alias '{args.alias}' -> '{args.collection}'", flush=True)

    print(f"Concluído. Total: {total} documentos na coleção '{args.collection}'.")


if __name__ == "__main__":
    main()
