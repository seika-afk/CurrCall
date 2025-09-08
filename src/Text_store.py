import os
from dotenv import load_dotenv
load_dotenv()

from Data_ingestion import Document
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS


def get_chunks(Document):
    chunk_list = [doc.page_content for doc in Document]
    text = "\n".join(chunk_list)
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "header1"),
            ("##", "header2"),
            ("###", "header3")
        ]
    )
    return splitter.split_text(text)


def vectWork(chunks_):
    # Use API key from .env
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )
    return FAISS.from_documents(chunks_, embeddings)


chunks_ = get_chunks(Document)
Vector_Store = vectWork(chunks_)
Vector_Store.save_local("faiss_index")

