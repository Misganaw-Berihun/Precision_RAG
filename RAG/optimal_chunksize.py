import sys, os
import nest_asyncio

nest_asyncio.apply()

from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    ServiceContext
)

from llama_index.core.evaluation import (
    DatasetGenerator,
    FaithfulnessEvaluator,
    RelevancyEvaluator
)

from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
Settings.embed_model = OpenAIEmbedding()

rpath = os.path.abspath('..')
if rpath not in sys.path:
    sys.path.insert(0, rpath)
    
from utility.env_manager import get_env_manager

import openai 
import time 

openai_key = get_env_manager()['openai_keys']['OPENAI_API_KEY']
openai.api_key = openai_key

def read_data(dir_path):
    reader = SimpleDirectoryReader("../data")
    return reader.load_data()

def generate_questions(doc):
    data_generation = DatasetGenerator.from_documents(doc) 
    eval_questions = data_generation.generate_questions_from_nodes(num=10)

    return eval_questions


def evaluate_response_time_and_accuracy(docs, chunk_size, overlap, faithfulness, relevancy, questions):
    total_response_time = 0
    total_faithfulness = 0
    total_relevancy = 0

    llm = OpenAI(model="gpt-3.5-turbo")
    service_context = ServiceContext.from_defaults(llm=llm, chunk_overlap= overlap, chunk_size=chunk_size)
    vector_index = VectorStoreIndex.from_documents(
        docs,
        service_context=service_context
    )

    query_engine = vector_index.as_query_engine()

    for question in questions:
        start_time = time.time()
        response_vector = query_engine.query(question)
        elapsed_time = time.time() - start_time
        
        faithfulness_result = faithfulness.evaluate_response(
            response=response_vector
        ).passing
        
        relevancy_result = relevancy.evaluate_response(
            query=question, response=response_vector
        ).passing

        total_response_time += elapsed_time
        total_faithfulness += faithfulness_result
        total_relevancy += relevancy_result

    num_questions = len(questions)
    average_response_time = total_response_time / num_questions
    average_faithfulness = total_faithfulness / num_questions
    average_relevancy = total_relevancy / num_questions

    return average_response_time, average_faithfulness, average_relevancy

def main():
    gpt = OpenAI(temperature=0, model="gpt-4")

    service_context = ServiceContext.from_defaults(llm=gpt)

    faithfulness = FaithfulnessEvaluator(service_context=service_context)
    relevancy = RelevancyEvaluator(service_context=service_context)

    file_path = '../data'
    docs = read_data(file_path)
    questions = generate_questions(docs)

    for chunk_size, overlap in [(128, 38), (256, 51), (512, 76), (1024, 102), (2048, 102)]:
        avg_time, avg_faithfulness, avg_relevancy = evaluate_response_time_and_accuracy(docs, chunk_size, overlap, faithfulness, relevancy, questions)
        print(f"Chunk size {chunk_size} & overlap {overlap}- Average Response time: {avg_time:.2f}s, Average Faithfulness: {avg_faithfulness:.2f}, Average Relevancy: {avg_relevancy:.2f}")


main()