from state.state import State
from services.rag_services import load_vectorstore, clean_text, rag_chain
from config.settings import TEMP_PDF_PATH
class RagNode:
    """
    Responsible for Retrieval Augmented Generation.
    """
    
    def __init__(self,model):
        self.llm = model
    
    def retrieve(self, state:State):
        """
        Retriever Node

        Args:
            state(dict) : The current graph state
        Returns:
            state(dict): New key added to state that returns documents whose value is the retrieved documents
        """
        
        query = state["query"]
        retriever = load_vectorstore(TEMP_PDF_PATH)
        docs = retriever.invoke(query)
        doc_texts = [clean_text(doc.page_content) for doc in docs]
        return {"documents":doc_texts}
    
    def process_docs(self,state:State)->dict:
        """_summary_

        Args:
            state (State): The current graph state

        Returns:
            state(dict): New key added to state, rag_generation that contains summary of retrieved documents.
        """
        
        question = state['query']
        documents = state['documents']
        generation = rag_chain(self.llm, documents, question)
        clean_generation = clean_text(generation)
        
        return {"rag_generation": clean_generation}