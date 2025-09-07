import os
from pathlib import Path
#from dotenv import load_dotenv
from langchain_groq import ChatGroq

class GroqLLM:
    """Initialise the model through Groq API."""
    
    def __init__(self, model_name: str = ""):
        #load_dotenv(dotenv_path=Path(__file__).parent/"../.env")
        self.model_name = model_name 
        self.api_key = os.getenv("GROQ_API_KEY")
        print(self.api_key)
        
    def get_llm_model(self):
        try:
            llm = ChatGroq(model_name = self.model_name, api_key = self.api_key)
            
        except Exception as e:
            raise ValueError(f"Error occurred with exception: {e}")
        return llm
    
    def get_llm_model_json(self):
        try:
            llm  = ChatGroq(model_name = self.model_name, api_key = self.api_key)
            llm_json = llm.with_structured_output(method="json_mode")
        except Exception as e:
            raise ValueError(f"Error occurred with exception: {e}")
        return llm_json

if __name__ == "__main__":
    model = GroqLLM(model_name= "openai/gpt-oss-20b").get_llm_model()
    print(model.invoke("What was my prior query?"))
    
            