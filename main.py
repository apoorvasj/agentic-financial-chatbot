from graph.graph_builder import GraphBuilder
import os
from LLMs.groqllm import GroqLLM
from IPython.display import Image, display
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

if __name__== "__main__":
    
    #load the environment variables.
    load_dotenv()
    
    model_name = os.getenv("GROQ_MODEL")
    model = GroqLLM(model_name).get_llm_model()
    model_json_mode = GroqLLM(model_name).get_llm_model_json()
    
    graph_builder = GraphBuilder(model,model_json_mode)
    graph = graph_builder.chatbot_build_graph()
    #query = "What is the current stock open price for Bajaj Finserv?"
    query = input("Enter your query")
    result=graph.invoke({"query":query})
    #display(Image(graph.get_graph().draw_mermaid_png()))
    print(result)