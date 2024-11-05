from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import chromadb
from config import *

# Define CONFIG dictionary


class VectorStore:
    def __init__(self, persist_directory=CONFIG['CHROMA_DB_DIR']):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=CONFIG['EMBEDDINGS_MODEL'],
            model_kwargs={'device': 'cpu'}
        )
        self.vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings
        )

    def add_texts(self, texts, metadatas=None):
        return self.vector_store.add_texts(texts=texts, metadatas=metadatas)

    def similarity_search(self, query, k=5):
        return self.vector_store.similarity_search(query, k=k)


