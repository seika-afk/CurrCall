from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
import yaml, os
import numpy as np

with open("params.yaml", "r") as f:
    config = yaml.safe_load(f)

class MiniLMEmbeddings:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts):
        return self.model.encode(texts, convert_to_numpy=True)

    def embed_query(self, text):
        return self.model.encode([text], convert_to_numpy=True)[0]

def get_retriever():
    embeddings = MiniLMEmbeddings()
    base_dir = os.path.dirname(__file__)
    faiss_path = os.path.join(base_dir, "faiss_index")
    
    vector_store = FAISS.load_local(
        faiss_path, 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": config.get("retrieving", {}).get("num_of_retrieved_docs", 5)
        }
    )
