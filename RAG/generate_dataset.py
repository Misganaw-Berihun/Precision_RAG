import os, sys
from openai import OpenAI

import nest_asyncio

nest_asyncio.apply()

print(sys.path)

rpath = os.path.abspath('..')
if rpath not in sys.path:
    sys.path.insert(0, rpath)

from ragas.testset.generator import TestsetGenerator
from llama_index.core import SimpleDirectoryReader
from ragas.testset.evolutions import simple, reasoning, multi_context

from langchain.document_loaders import (
    PDFMinerLoader,
    DirectoryLoader
)

def read_data(file_path):
    documents = DirectoryLoader(file_path, glob="**/*.pdf", loader_cls=PDFMinerLoader).load()
    return documents
    for document in documents:
        document.metadata['file_name'] = document.metadata['source']
    return documents


def generate_testset(documents):
    generator = TestsetGenerator.with_openai() 
    distributions = {
        simple: 0.5,
        multi_context: 0.4,
        reasoning: 0.1
    }
    testset = generator.generate_with_langchain_docs(documents, test_size=10, distributions=distributions)
    return testset.to_pandas()
    

def main():
    file_path = '../data'
    documents = read_data(file_path)
    testset = generate_testset(documents)
    testset.to_csv('testset.csv')
    print(testset) 

main()