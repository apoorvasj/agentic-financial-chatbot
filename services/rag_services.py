from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import CHUNK_OVERLAP, CHUNK_SIZE, HF_MODEL
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain import hub
from langchain_cohere import CohereEmbeddings
from services.prompts import rag_prompt
from langchain_core.prompts import ChatPromptTemplate

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
    embeddings = embeddings = CohereEmbeddings(
    model="embed-english-v3.0",
)
    vectorstore = Chroma.from_documents(splitted, embeddings)
    
    return vectorstore.as_retriever()

def rag_chain(llm, docs, question):
    prompt = rag_prompt()
    rag_summary_prompt = ChatPromptTemplate.from_messages([
            ("system",prompt),
            ("human","Content: {context}. User question: {question}")
        ])
    
    rag_chain = rag_summary_prompt | llm | StrOutputParser()
    
    generation = rag_chain.invoke({"context":docs,"question":question})
    return generation


def clean_text(text):
    return text.encode("utf-8", "ignore").decode("utf-8", "ignore")
    
    
    