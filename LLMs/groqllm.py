import os
from pathlib import Path
#from dotenv import load_dotenv
from langchain_groq import ChatGroq
import streamlit as st

class GroqLLM:
    """Initialise the model through Groq API."""
    
    def __init__(self,user_controls_input):
        #load_dotenv(dotenv_path=Path(__file__).parent/"../.env")
        #self.model_name = model_name 
        #self.api_key = os.getenv("GROQ_API_KEY")
        #print(self.api_key)
        
        #class variables
        self.user_controls_input= user_controls_input
        
    def get_llm_model(self):
        try:
            #llm = ChatGroq(model_name = self.model_name, api_key = self.api_key)
            groq_api_key= self.user_controls_input["GROQ_API_KEY"]
            selected_groq_model= self.user_controls_input["selected_llm"]
            if groq_api_key=='' and os.environ["GROQ_API_KEY"]=='':
                st.error('Please enter the Groq API key.')
            llm= ChatGroq(model=selected_groq_model,api_key=groq_api_key,model_kwargs={
        })
            
        except Exception as e:
            raise ValueError(f"Error occurred with exception: {e}")
        return llm
    
    def get_llm_model_json(self):
        try:
            groq_api_key= self.user_controls_input["GROQ_API_KEY"]
            selected_groq_model= self.user_controls_input["selected_llm"]
            llm  = ChatGroq(model_name = selected_groq_model, api_key = groq_api_key)
            llm_json = llm.with_structured_output(method="json_mode")
        except Exception as e:
            raise ValueError(f"Error occurred with exception: {e}")
        return llm_json

if __name__ == "__main__":
    model = GroqLLM(model_name= "openai/gpt-oss-20b").get_llm_model()
    print(model.invoke("What was my prior query?"))
    
            