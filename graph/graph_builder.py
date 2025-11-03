from state.state import State
from langgraph.graph import StateGraph, START, END
from nodes.chatbot_node import BasicChatbotNode
from nodes.rag_node import RagNode
from services.tools import get_tools
from langgraph.prebuilt import ToolNode, tools_condition
from services.services import decide_to_generate, correct_hallucination
from services.memory.postgres import create_checkpointer
from langgraph.checkpoint.postgres import PostgresSaver

class GraphBuilder:
    def __init__(self,model, model_json):
        self.llm = model 
        self.llm_json = model_json
        self.tools = get_tools()
        self.graph_builder = StateGraph(State)
    
    def chatbot_build_graph(self):
        """
        Builds a chatbot graph using LangGraph
        """
        self.basic_chatbot_node = BasicChatbotNode(self.llm,self.llm_json)
        self.rag_node  = RagNode(self.llm)
        
        #add nodes
        #self.graph_builder.add_node("router", self.basic_chatbot_node.router)
        self.graph_builder.add_node("tool_node",self.basic_chatbot_node.llm_tool)
        self.graph_builder.add_node("tools",ToolNode(self.tools))
        self.graph_builder.add_node("tool_summariser", self.basic_chatbot_node.llm_summariser)
        self.graph_builder.add_node("QnA_node",self.basic_chatbot_node.llm_basic)
        self.graph_builder.add_node("Retriever",self.rag_node.retrieve)
        self.graph_builder.add_node("RAG_summariser",self.rag_node.process_docs)
        self.graph_builder.add_node("grade_docs",self.basic_chatbot_node.grade_docs)
        self.graph_builder.add_node("rewrite",self.basic_chatbot_node.rewrite_query)
        self.graph_builder.add_node("check_hallucination",self.basic_chatbot_node.grade_hallucination)
        
        #add edges
        #self.graph_builder.add_edge(START, "tool_node")
        #self.graph_builder.add_conditional_edges("tool_node",tools_condition)
        #self.graph_builder.add_edge("tools","summariser")
        #self.graph_builder.add_edge("summariser",END)    
        #self.graph_builder.add_edge("tools",END)
 
        self.graph_builder.add_conditional_edges(START,
                                                 self.basic_chatbot_node.router,
                                                 {
                                                     "apisearch": "tool_node",
                                                     "vectorstore":"Retriever",
                                                     "general":"QnA_node"
                                                 })
        self.graph_builder.add_edge("tool_node","tools")
        self.graph_builder.add_edge("tools","tool_summariser")
        #self.graph_builder.add_edge("Retriever", "RAG_summariser")
        self.graph_builder.add_edge("Retriever","grade_docs")
        self.graph_builder.add_conditional_edges("grade_docs",decide_to_generate,{
            "rewrite_query":"rewrite",
            "generate":"RAG_summariser"
        })
        self.graph_builder.add_edge("rewrite","Retriever")
        #self.graph_builder.add_edge("RAG_summariser", END)
        self.graph_builder.add_edge("RAG_summariser","check_hallucination")
        self.graph_builder.add_conditional_edges("check_hallucination",correct_hallucination,{
            "regenerate":"RAG_summariser",
            "end":END
        })
        self.graph_builder.add_edge("tool_summariser",END)
        self.graph_builder.add_edge("QnA_node",END)
        
        conn = create_checkpointer()
        checkpointer = PostgresSaver(conn)
        checkpointer.setup()
        
        return self.graph_builder.compile(checkpointer = checkpointer)