from __future__ import annotations

from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.http import models as qm

from indexer.point_ids import to_qdrant_point_id


def ensure_collection(
    client: QdrantClient,
    collection_name: str,
    vector_size: int,
    distance: qm.Distance = qm.Distance.COSINE,
) -> None:
    exists = False
    try:
        client.get_collection(collection_name)
        exists = True
    except Exception:
        exists = False
    if not exists:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=qm.VectorParams(size=vector_size, distance=distance),
        )


def upsert_batch(
    client: QdrantClient,
    collection_name: str,
    points: list[qm.PointStruct],
) -> None:
    client.upsert(collection_name=collection_name, points=points, wait=True)


def set_alias(client: QdrantClient, alias_name: str, collection_name: str) -> None:
    """Aponta o alias para a coleção (substitui se já existir)."""
    ops: list[qm.DeleteAliasOperation | qm.CreateAliasOperation] = [
        qm.DeleteAliasOperation(
            delete_alias=qm.DeleteAlias(alias_name=alias_name),
        ),
        qm.CreateAliasOperation(
            create_alias=qm.CreateAlias(
                alias_name=alias_name,
                collection_name=collection_name,
            ),
        ),
    ]
    try:
        client.update_collection_aliases(change_aliases_operations=ops)
    except Exception:
        client.update_collection_aliases(
            change_aliases_operations=[
                qm.CreateAliasOperation(
                    create_alias=qm.CreateAlias(
                        alias_name=alias_name,
                        collection_name=collection_name,
                    ),
                )
            ]
        )


def build_point(vector: list[float], payload: dict[str, Any]) -> qm.PointStruct:
    """Usa payload['id'] como ID logico; ID interno do Qdrant e uint ou UUID."""
    raw = payload.get("id")
    if raw is None:
        raise ValueError("payload sem campo 'id'")
    qid = to_qdrant_point_id(raw)
    return qm.PointStruct(id=qid, vector=vector, payload=payload)
