from state.state import State
class RagNode:
    """
    Responsible for Retrieval Augmented Generation.
    """
    
    def retrieve(self, state:State):
        """
        Retriever Node

        Args:
            state(dict) : The current graph state
        Returns:
            state(dict): New key added to state that returns documents whose value is the retrieved documents
        """
        
        query = state["query"]
        retriever = load_vectorstore()
        docs = retriever.invoke(query)
        doc_texts = [clean_text(doc.page_content) for doc in docs]
        return {"documents":doc_texts}