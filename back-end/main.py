import os, sys
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS

rpath = os.path.abspath('..')
if rpath not in sys.path:
    sys.path.insert(0, rpath)

from utility.document_reader import load_document
from utility.read_file import file_reader, json_parser
from prompt_reranking.elo_rating import calculate_elo
from evaluation._data_generation import generate_the_prompts, save_json

from RAG.rag_app import get_vector_index, get_response, get_context_from_db, read_data

app = Flask(__name__)
CORS(app)

@app.route('/api/generate_prompts', methods=['POST'])
def generate_prompts():
    try:
        objectives = request.form.getlist('objectives')  
        expected_outputs = request.form.getlist('expectedOutputs') 
        temp_dir = tempfile.TemporaryDirectory()

        # docs = []
        # for file_key in request.files:
        #     uploaded_file = request.files[file_key]
        #     temp_filepath = os.path.join(temp_dir.name, uploaded_file.filename)
        #     uploaded_file.save(temp_filepath)
        #     docs.extend(load_document(temp_filepath))
        # print(docs)
        path = '../data'
        docs = read_data(path)
        print(objectives[0], expected_outputs[0])
        index = get_vector_index(docs)
        contexts = get_context_from_db(objectives[0], index)
        
        sequence = [context.get_text() for context in contexts]
        context = ' '.join(sequence)

        prompt = file_reader('../prompts/automatic-prompt-generation.txt')
        prompt = str(prompt) 
        prompts = generate_the_prompts(prompt, context, objectives[0], expected_outputs[0])

        file_path = "../prompts-generated/prompts.json"
        save_json(prompts, file_path)
        return jsonify({"msg": "prompts created succesfully"})

    except Exception as e:
        print("Error generating prompts:", str(e))
        return jsonify({"error": "Failed to generate prompts"}), 500

@app.route('/api/prompts',  methods=['get'])
def prompts():
    path = '../prompts-generated/prompts.json'
    prompts_str = file_reader(path)
    prompts = json_parser(prompts_str)
    
    elo_rating = calculate_elo(prompts=prompts)
    sorted_ratings = sorted(prompts, key=lambda x: elo_rating[x], reverse=True)[:4]
    return jsonify(
        {
            "prompts": sorted_ratings
        }
    )




if __name__ == '__main__':
    app.run(debug=True)
