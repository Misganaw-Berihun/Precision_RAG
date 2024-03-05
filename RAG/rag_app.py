import os, sys
from openai import OpenAI

rpath = os.path.abspath('..')
if rpath not in sys.path:
    sys.path.insert(0, rpath)
    
from utility.env_manager import get_env_manager
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document, StorageContext, Settings
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding

openai_key = get_env_manager()['openai_keys']['OPENAI_API_KEY']

def read_data(file_path):
    documents = SimpleDirectoryReader(file_path).load_data()
    return documents

def get_vector_index(documents):
    Settings.chunk_size = 1024
    Settings.chunk_overlap = 102
    Settings.embed_model = OpenAIEmbedding()

    vector_store = MilvusVectorStore(
        dim=1536, 
        overwrite=True
        )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context,
        )

    return index

def get_context_from_db(question, index):
    retriever = index.as_retriever(similarity_top_k=5)
    nodes = retriever.retrieve(question)
    return nodes


def get_response(question, index):
    query_engine = index.as_query_engine(similarity_top_k=5)
    response = query_engine.query(question)
    return str(response)
