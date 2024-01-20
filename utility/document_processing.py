import ssl
from dotenv import load_dotenv
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import os
import weaviate

def configure_ssl():
    ssl._create_default_https_context = ssl._create_unverified_context

def load_environment_variables():
    load_dotenv()

def load_documents(directory_path='./', glob_pattern="**/*.pdf"):
    loader = DirectoryLoader(directory_path, glob=glob_pattern)
    return loader.load()

def split_documents(data, chunk_size=512, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(data)

def configure_weaviate_client():
    auth_config = weaviate.AuthApiKey(api_key=os.environ["WEAVIATE_API_KEY"])
    
    client = weaviate.Client(
        url="https://rag-l4x00jnr.weaviate.network",
        additional_headers={"X-OpenAI-Api-Key": os.environ["OPENAI_API_KEY"]},
        auth_client_secret=auth_config,
        startup_period=10
    )

    return client

def define_weaviate_schema(client):
    client.schema.delete_all()
    client.schema.get()

    schema = {
        "classes": [
            {
                "class": "Chatbot",
                "description": "Documents for chatbot",
                "vectorizer": "text2vec-openai",
                "moduleConfig": {"text2vec-openai": {"model": "ada", "type": "text"}},
                "properties": [
                    {
                        "dataType": ["text"],
                        "description": "The content of the paragraph",
                        "moduleConfig": {
                            "text2vec-openai": {
                                "skip": False,
                                "vectorizePropertyName": False,
                            }
                        },
                        "name": "content",
                    },
                ],
            },
        ]
    }

    client.schema.create(schema)

def configure_openai_embeddings():
    return OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])

def configure_weaviate_vectorstore(client):
    return Weaviate(client, "Chatbot", "content", attributes=["source"])

def main():
    configure_ssl()
    load_environment_variables()

    documents = load_documents('./', glob_pattern="**/*.pdf")
    split_docs = split_documents(documents)

    weaviate_client = configure_weaviate_client()
    define_weaviate_schema(weaviate_client)

    openai_embeddings = configure_openai_embeddings()
    
    weaviate_vectorstore = configure_weaviate_vectorstore(weaviate_client)
    text_meta_pair = [(doc.page_content, doc.metadata) for doc in split_docs]
    texts, meta = list(zip(*text_meta_pair))
    weaviate_vectorstore.add_texts(texts, meta)

if __name__ == "__main__":
    main()
