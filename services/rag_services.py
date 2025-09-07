from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from config.settings import CHUNK_OVERLAP, CHUNK_SIZE, HF_MODEL
from langchain_chroma import Chroma

"""Provides RAG-related helper functions.
"""

def load_vectorstore(PDF_PATH):
    """Function to process a document.
    1. Load the document.
    2. Split or chunk the document into smaller pieces.
    3. Embed the document- convert to vectors. The semantic meaning is maintained in these vectors.
    4. Store in a vectorstore
    """
    
    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size = CHUNK_SIZE, chunk_overlap = CHUNK_OVERLAP)
    splitted = splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name = HF_MODEL)
    vectorstore = Chroma.from_documents(splitted, embeddings)
    
    return vectorstore.as_retriever()

def rag_chain(llm, docs, question):
    prompt = hub.pull()
    
    