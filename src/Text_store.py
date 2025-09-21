import os
from dotenv import load_dotenv
from data_ingestion import Document  

from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document as LC_Document  
import json

load_dotenv()

def get_chunks(documents):

    chunk_list = [doc.page_content for doc in documents]
    text = "\n".join(chunk_list)

    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "header1"),
            ("##", "header2"),
            ("###", "header3")
        ]
    )

    return splitter.split_text(text)
 

def vectorWork(chunks_):
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vector_store = FAISS.from_documents(chunks_, embeddings)
    return vector_store


chunks_ = get_chunks(Document)
Vector_store = vectorWork(chunks_)
Vector_store.save_local("faiss_store")
print("FAISS index created and saved locally!")
