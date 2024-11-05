from dotenv import load_dotenv
import os

load_dotenv()

CONFIG = {
    'GROQ_API_KEY': os.getenv('GROQ_API_KEY'),
    'GITHUB_TOKEN': os.getenv('GITHUB_TOKEN'),
    'LLAMA_MODEL': 'llama-3.1-70b-versatile',
    'EMBEDDINGS_MODEL': 'sentence-transformers/all-mpnet-base-v2',
    'CHROMA_DB_DIR': './chroma_db',
    'CACHE_DIR': './cache',
}
