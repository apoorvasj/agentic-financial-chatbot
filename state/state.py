from typing import Annotated, List
from langgraph.graph import add_messages
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from langchain_core.messages import AnyMessage

class State(TypedDict):
    """
    Represents the structure of the state used in the graph.
    """
    query: str = "" #user query
    route: str="" #route decided by route node
    response: str = "" #llm response
    messages: str = ""
    documents: str = ""
    

