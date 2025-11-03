from state.state import State
from services.tools import get_tools
from services.prompts import router_prompt, tool_node_prompt, summariser_prompt
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from services.grade_documents import grade_documents
from services.hallucination_grader import grade_hallucination_helper
from services.tools import rewriter

class BasicChatbotNode:
    """
    Chatbot Implementation
    """
    
    def __init__(self,model,model_json):
        self.llm = model
        self.llm_json = model_json
    
    def llm_basic(self,state:State):
        """
        A basic chatbot node that answers general finance queries.
        """
        prompt= """You are a financial query chatbot. Answer the questions related to finances or stocks and financial regulations. For
             any other unrelated query state your purpose clearly."""
        response = self.llm.invoke(
            [SystemMessage(content= prompt)]+
            [HumanMessage(content=state["query"])]
        )
        
        return{"response":response}
        
    def llm_summariser(self,state:State):
        """A summariser after a tool/API call is made."""
        llm_base = self.llm
        system = summariser_prompt()
        summary_prompt = ChatPromptTemplate.from_messages([
            ("system",system),
            ("human","Content: {messages}. User question: {query}")
        ]
        )
        summariser = summary_prompt|llm_base
        response = summariser.invoke({'query':state["query"],'messages':state["messages"][-1].content})
        return {"response":response}
    
    def llm_tool(self, state:State):
        """
        LLM with tools node
        Decides which tool to call
        """
        tools = get_tools()
        llm_tooled = self.llm.bind_tools(tools)
        response = llm_tooled.invoke(
            [SystemMessage(content= tool_node_prompt())]+
            [HumanMessage(content=state["query"])]
        )
        return {"messages":[response]}
    
    def router(self,state:State):
        """
        Router node to decide whether to do an API search, perform RAG or answer a general query.
        """
        
        llm_router = self.llm_json
        route = llm_router.invoke(
            [SystemMessage(content= router_prompt())]+
            [HumanMessage(content=state["query"])]
        )
        print(route)
        if(route["datasource"]=="apisearch"):
            return "apisearch"
        elif(route["datasource"]=="vectorstore"):
            return "vectorstore"
        else:
            return "general"
    
    def grade_docs(self,state):
        """
        Determines whether the retrieved documents are relevant to the question.

        Args:
            state (dict): The current graph state

        Returns:
            state(dict): Updates documents key with only filtered relevant documents.
        """

        question= state['query']
        documents= state["documents"]

        #Give a score for each doc.
        filtered_docs= []
        #create an instance of a retrieval grader.
        retrieval_grader= grade_documents(self.llm)
        for d in documents:
            score= retrieval_grader.invoke(
                {'question':question, 'document':d}
            )

            grade= score.binary_score
            
            if(grade=="yes"):
                filtered_docs.append(d)
        re_gen_req= "no" if filtered_docs else "yes"
        return {"documents": filtered_docs, "re_gen_required":re_gen_req}
    
    def rewrite_query(self,state:State):
        """
        Transform the query to produce a better question.

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Updates question key with a re-phrased question
        """
        print('REWRITING QUERY')
        question= state['query']
        

        rewrite_query= rewriter(self.llm)
        
        better_question= rewrite_query.invoke({'question',question})

        return {'query': better_question}
    
    def grade_hallucination(self, state:State):
        """
        Determines whether the generation is grounded in the document and answers question.

        Args:
            state (dict): The current graph state

        Returns:
            str: Decision for next node to call
        """

        
        documents = state["documents"]
        generation= state["response"]

        grader= grade_hallucination_helper(self.llm)
        score= grader.invoke({
            "documents":documents, "generation": generation
        })
        grade= score.binary_score
        
        #if we have regenerated query 5 times, no need to continue further.
        limit = state.get("re_gen_limit", 0)
        if(limit>5):
            return{"hallucination_present":"no","re_gen_limit":state["re_gen_limit"]}

        return{"hallucination_present":grade, "re_gen_limit":limit+1}
    
        
        