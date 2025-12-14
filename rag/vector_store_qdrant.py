from typing import Any, Optional, List, Dict
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

class QdrantVectorStore:
    def __init__(self, client: Any, collection_name: str, embedder: Any = None):
        self.client = client
        self.collection_name = collection_name
        self.embedder = embedder

    def search(self, query_text: str, k: int = 5, vector_name: str = "Default vector") -> List[str]:
        try:
            if self.embedder is None:
                raise ValueError("Embedder is not initialized. Cannot encode query text.")

            query_vector_raw = self.embedder.encode_query(query_text)

            if isinstance(query_vector_raw, np.ndarray) and query_vector_raw.ndim == 2:
                query_vector = query_vector_raw[0]
            else:
                query_vector = query_vector_raw

            if isinstance(query_vector, np.ndarray):
                query_vector = query_vector.tolist()

            response: Any = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=k,
                with_payload=True
            )

            results: List[str] = []
            for hit in response.points:
                payload: Dict[str, Any] = hit.payload or {}
                text_content: Optional[str] = payload.get("text")
                if text_content is not None:
                    results.append(str(text_content))
            return results
        except Exception as e:
            logging.error(f"Error during vector search: {e}")
            return ["⚠️ Something went wrong while retrieving information. Please check your internet connection and try again."]
