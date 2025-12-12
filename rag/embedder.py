import numpy as np
from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts, batch_size=32):
        vectors = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            vectors.append(self.model.encode(batch, convert_to_numpy=True))
        return np.vstack(vectors)

    def encode_query(self, query: str):
        return self.model.encode([query], convert_to_numpy=True)
