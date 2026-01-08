import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent/"../.env")
  
HF_MODEL = "sentence-transformers/all-MPNet-base-v2"
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50
TEMP_PDF_PATH = "./temp.pdf"
DB_URI= os.getenv('DB_URI')

if __name__=='__main__':
    print(DB_URI)
    