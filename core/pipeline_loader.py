# core/pipeline_loader.py
import streamlit as st
from rag.embedder import Embedder
from rag.qa_pipeline import QAPipeline
from rag.llm_client import LLMClient
from rag.vector_store_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient


@st.cache_resource(show_spinner=False)
def init_pipeline(Config):
    # Qdrant client
    qdrant_client = QdrantClient(
        url=Config.QDRANT_URL,
        api_key=Config.QDRANT_API_KEY
    )

    # Embedder (your existing Embedder class)
    embedder = Embedder(Config.EMBEDDING_MODEL)

    # Qdrant vector store
    vector_store = QdrantVectorStore(
        client=qdrant_client,
        collection_name=Config.QDRANR_COLLECTION_NAME,
         embedder=embedder
    )

    # LLM client
    llm_client = LLMClient(api_key=Config.GEMINI_API_KEY, model=Config.LLM_NAME)

    # Initialize QAPipeline
    return QAPipeline(embedder, vector_store, llm_client)
