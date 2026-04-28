"""
Embedding Engine — Hybrid Multilingual CLIP.
Uses 'clip-ViT-B-32-multilingual-v1' for multilingual TEXT.
Uses 'clip-ViT-B-32' for IMAGE.
Both share the same vector space, enabling multilingual text-to-image search.
"""

import io
import base64
from PIL import Image

def _load_text_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer('sentence-transformers/clip-ViT-B-32-multilingual-v1')

def _load_image_model():
    from sentence_transformers import SentenceTransformer
    # The original CLIP model supports 'image' modality
    return SentenceTransformer('clip-ViT-B-32')

def _load_rerank_model():
    from sentence_transformers import CrossEncoder
    # Using a highly compatible and standard model to avoid identifier errors
    return CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')


class EmbeddingEngine:
    _text_model = None
    _image_model = None
    _rerank_model = None

    @classmethod
    def text_model(cls):
        if cls._text_model is None:
            print("[EmbeddingEngine] Loading Multilingual Text model...")
            cls._text_model = _load_text_model()
        return cls._text_model

    @classmethod
    def image_model(cls):
        if cls._image_model is None:
            print("[EmbeddingEngine] Loading Vision CLIP model...")
            cls._image_model = _load_image_model()
        return cls._image_model

    @classmethod
    def rerank_model(cls):
        if cls._rerank_model is None:
            print("[EmbeddingEngine] Loading Re-ranking model (mMiniLM)...")
            cls._rerank_model = _load_rerank_model()
        return cls._rerank_model

    @classmethod
    def embed_text(cls, text: str) -> list:
        """Return a 512-dim embedding for text using the multilingual encoder."""
        vec = cls.text_model().encode(text, convert_to_numpy=True)
        return vec.tolist()

    @classmethod
    def embed_text_batch(cls, texts: list) -> list:
        """Return 512-dim embeddings for a list of texts."""
        if not texts: return []
        vecs = cls.text_model().encode(texts, convert_to_numpy=True, batch_size=32, show_progress_bar=False)
        return vecs.tolist()

    @classmethod
    def embed_image_bytes(cls, image_bytes: bytes) -> list:
        """Return a 512-dim embedding for image using the vision encoder."""
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        vec = cls.image_model().encode(image, convert_to_numpy=True)
        return vec.tolist()

    @classmethod
    def embed_image_batch(cls, images: list) -> list:
        """Return 512-dim embeddings for a list of PIL Images or file paths."""
        if not images: return []
        vecs = cls.image_model().encode(images, convert_to_numpy=True, batch_size=32, show_progress_bar=False)
        return vecs.tolist()

    @classmethod
    def embed_image_b64(cls, b64_string: str) -> list:
        raw = base64.b64decode(b64_string)
        return cls.embed_image_bytes(raw)

    @classmethod
    def embed_image_url(cls, url: str) -> list:
        import urllib.request
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read()
        return cls.embed_image_bytes(raw)

    @classmethod
    def rerank(cls, query: str, documents: list) -> list:
        """
        Re-rank a list of text documents against a query using Cross-Encoder.
        Returns a list of scores (higher is better).
        """
        if not documents: return []
        scores = cls.rerank_model().predict([[query, doc] for doc in documents])
        # Normalize scores to 0-1 range roughly (CrossEncoder output can vary)
        # Using sigmoid if needed, but standard predict is often enough for ranking.
        return scores.tolist()

    @staticmethod
    def camera_to_text(camera: dict) -> str:
        parts = []
        if camera.get('name'):
            parts.append(f"Tên camera: {camera['name']}.")
        if camera.get('location'):
            parts.append(f"Vị trí: {camera['location']}.")
        if camera.get('status'):
            parts.append(f"Trạng thái: {camera['status']}.")
        if camera.get('resolution'):
            parts.append(f"Độ phân giải: {camera['resolution']}.")
        
        if not parts:
            return f"Camera quan sát mã số {camera.get('id', 'mới')}."
        return ' '.join(parts)
