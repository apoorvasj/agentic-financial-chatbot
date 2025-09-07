from state.state import State
from langgraph.graph import StateGraph, START, END
from nodes.chatbot_node import BasicChatbotNode
from services.tools import get_tools
from langgraph.prebuilt import ToolNode, tools_condition

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
        
        #add nodes
        #self.graph_builder.add_node("router", self.basic_chatbot_node.router)
        self.graph_builder.add_node("tool_node",self.basic_chatbot_node.llm_tool)
        self.graph_builder.add_node("tools",ToolNode(self.tools))
        self.graph_builder.add_node("tool_summariser", self.basic_chatbot_node.llm_summariser)
        self.graph_builder.add_node("QnA_node",self.basic_chatbot_node.llm_basic)
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
                                                     "vectorstore":"QnA_node",
                                                     "general":"QnA_node"
                                                 })
        self.graph_builder.add_edge("tool_node","tools")
        self.graph_builder.add_edge("tools","tool_summariser")
        self.graph_builder.add_edge("tool_summariser",END)
        self.graph_builder.add_edge("QnA_node",END)
            
        return self.graph_builder.compile()