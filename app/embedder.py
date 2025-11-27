from sentence_transformers import SentenceTransformer
import numpy as np

# Load a free, local embedding model
# This downloads once, then is cached
_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str) -> np.ndarray:
    """
    Returns a numpy vector embedding for the given text using a local model.
    No API key required.
    """
    if not text:
        return np.zeros(_model.get_sentence_embedding_dimension(), dtype=float)

    text = text.replace("\n", " ")
    emb = _model.encode([text])[0]  # shape: (dim,)
    return np.array(emb, dtype=float)
