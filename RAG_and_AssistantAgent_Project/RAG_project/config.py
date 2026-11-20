import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path


load_dotenv(find_dotenv())

EMBED_MODEL = os.getenv("openai_embedding_model")
API_key = os.getenv("OPENAI_API_KEY")
CHAT_MODEL = os.getenv("openai_model")

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "chroma_db"
COLLECTION_name = "project1_RAG"

PDF_path = DATA_DIR / "Transformers_Architecture.pdf"
TextFile_path = DATA_DIR / "transformers_notes.txt"

CHUNK_SIZE=800
CHUNK_OVERLAP=150
TOP_K=4
Fetch_K=10
lambda_mult=0.5
Temperature = 0.1
Max_Tokens = 500 