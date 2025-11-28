from sentence_transformers import SentenceTransformer
import numpy as np
_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str) -> np.ndarray:
   
    if not text:
        return np.zeros(_model.get_sentence_embedding_dimension(), dtype=float)

    text = text.replace("\n", " ")
    emb = _model.encode([text])[0]  
    return np.array(emb, dtype=float)
