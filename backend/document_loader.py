import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CHROMA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")

def get_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    if os.path.exists(CHROMA_DIR):
        print("Loading existing Chroma vector store...")
        return Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    
    print("Creating new Chroma vector store...")
    loader = PyPDFDirectoryLoader(DATA_DIR)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    
    return vectorstore
