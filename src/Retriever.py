from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import yaml, os

with open("params.yaml", "r") as f:
    config = yaml.safe_load(f)

def get_retriever():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    base_dir = os.path.dirname(__file__)
    faiss_path = os.path.join(base_dir, "faiss_index")
    vector_store = FAISS.load_local(faiss_path, embeddings, allow_dangerous_deserialization=True)
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": config.get("retrieving", {}).get("num_of_retrieved_docs", 5)}
    )
