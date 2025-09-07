from state.state import State
from services.tools import get_tools
from services.prompts import router_prompt, tool_node_prompt, summariser_prompt
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate

class BasicChatbotNode:
    """
    Chatbot Implementation
    """
    
    def __init__(self,model,model_json):
        self.llm = model
        self.llm_json = model_json
    
    def llm_basic(self,state:State):
        return{"response":[self.llm.invoke(state["query"])]}
        
    def llm_summariser(self,state:State):
        #regular LLM node
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
        #LLM with tools node
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
    
        
        