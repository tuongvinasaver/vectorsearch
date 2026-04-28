"""
Vector Store — ChromaDB wrapper for camera embeddings.
Uses cosine similarity. Persists to data/chroma/ (file-based).
"""

import os


def _chroma_dir():
    base = os.path.join(os.path.dirname(__file__), 'data', 'chroma')
    os.makedirs(base, exist_ok=True)
    return base


class VectorStore:
    _client = None
    _collection = None
    COLLECTION = 'cameras'

    # ── Client / collection ────────────────────────────────────────────────────
    @classmethod
    def _get_client(cls):
        if cls._client is None:
            import chromadb
            cls._client = chromadb.PersistentClient(path=_chroma_dir())
        return cls._client

    @classmethod
    def collection(cls):
        if cls._collection is None:
            client = cls._get_client()
            cls._collection = client.get_or_create_collection(
                name=cls.COLLECTION,
                metadata={
                    'hnsw:space': 'cosine',  # Best for normalized CLIP vectors
                    'hnsw:construction_ef': 256,  # Higher accuracy during indexing
                    'hnsw:M': 32,  # More connections per node for better recall
                    'hnsw:batch_size': 100, # Faster bulk processing
                    'hnsw:sync_threshold': 1000 # Performance boost for larger datasets
                },
            )
        return cls._collection

    # ── Write ──────────────────────────────────────────────────────────────────
    @classmethod
    def upsert(cls, camera_id: int, embedding: list, metadata: dict):
        """Add or replace a camera vector. metadata must be flat str/int/float."""
        safe_meta = {k: (str(v) if v is not None else '') for k, v in metadata.items()}
        cls.collection().upsert(
            ids=[str(camera_id)],
            embeddings=[embedding],
            metadatas=[safe_meta],
        )

    @classmethod
    def upsert_batch(cls, ids: list, embeddings: list, metadatas: list):
        """Batch add or replace camera vectors."""
        if not ids: return
        safe_metadatas = []
        for meta in metadatas:
            safe_metadatas.append({k: (str(v) if v is not None else '') for k, v in meta.items()})
        
        cls.collection().upsert(
            ids=[str(i) for i in ids],
            embeddings=embeddings,
            metadatas=safe_metadatas,
        )

    @classmethod
    def delete(cls, camera_id: int):
        try:
            cls.collection().delete(ids=[str(camera_id)])
        except Exception:
            pass  # not indexed — that's fine

    # ── Read ───────────────────────────────────────────────────────────────────
    @classmethod
    def count(cls) -> int:
        return cls.collection().count()

    @classmethod
    def search(cls, embedding: list, n_results: int = 10, where: dict = None) -> list:
        """
        Returns a list of dicts:
          { 'camera_id': int, 'score': float, 'metadata': dict, 'embedding': list }
        """
        total = cls.count()
        if total == 0:
            return []

        n = min(n_results, total)
        raw = cls.collection().query(
            query_embeddings=[embedding],
            n_results=n,
            where=where,
            include=['metadatas', 'distances', 'embeddings'],
        )

        results = []
        for i in range(len(raw['ids'][0])):
            cam_id = raw['ids'][0][i]
            distance = raw['distances'][0][i]
            meta = raw['metadatas'][0][i]
            emb = raw['embeddings'][0][i]
            if hasattr(emb, 'tolist'):
                emb = emb.tolist()

            # ChromaDB cosine distance is `1 - cos_sim`.
            cos_sim = 1.0 - distance
            similarity = round(max(0.0, min(1.0, cos_sim)), 4)
            
            results.append({
                'camera_id': int(cam_id),
                'score': similarity,
                'distance': distance,
                'metadata': meta,
                'embedding': emb
            })

        return results

