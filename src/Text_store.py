import os
from dotenv import load_dotenv
from data_ingestion import Document  

from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document as LC_Document  #

load_dotenv()

def get_chunks(documents):
    """
    Splits documents based on Markdown headers (#, ##, ###)
    """
    chunk_list = [doc.page_content for doc in documents]
    text = "\n".join(chunk_list)
    
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "header1"),
            ("##", "header2"),
            ("###", "header3")
        ]
    )
    
    chunks = splitter.split_text(text)
    # Convert to LangChain Document objects
    lc_chunks = [LC_Document(page_content=chunk) for chunk in chunks]
    return lc_chunks

def vectorWork(documents, use_local=True):
    """
    Creates a FAISS vector store from document chunks
    """
    chunks_ = get_chunks(documents)
    
    if use_local:
        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    else:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.getenv("GEMINI_API_KEY")
        )
    
    vector_store = FAISS.from_documents(chunks_, embeddings)
    return vector_store

# Example: create/load your list of Document objects
docs = [Document(page_content="Your first text"), Document(page_content="Second text here")]

Vector_store = vectorWork(docs, use_local=True)
Vector_store.save_local("faiss_store")
print("FAISS index created and saved locally!")
