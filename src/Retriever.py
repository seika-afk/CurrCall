from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import yaml
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

with open("params.yaml", 'r') as f:
    config = yaml.safe_load(f)

# Pass the API key explicitly from .env
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

Vector_Stores = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = Vector_Stores.as_retriever(
    search_type="similarity",
    search_kwargs={"k": config["retrieving"]["num_of_retrieved_docs"]}
)

