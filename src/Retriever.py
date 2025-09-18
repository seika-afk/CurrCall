from langchain_community.vectorstores import FAISS
import yaml

with open("params.yaml", "r") as f:
    config = yaml.safe_load(f)

Vector_Stores = FAISS.load_local(
    "faiss_index",
    embeddings=None,  
    allow_dangerous_deserialization=True
)

retriever = Vector_Stores.as_retriever(
    search_type="similarity",
    search_kwargs={"k": config["retrieving"]["num_of_retrieved_docs"]}
)
