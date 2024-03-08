import os
import json

def file_reader(path: str) -> str:
    fname = os.path.join(path)
    with open(fname, 'r') as f:
        system_message = f.read()
    return system_message

def json_parser(json_string: str):
    prompts_data = json.loads(json_string)
    prompts = [item['prompt'] for item in prompts_data]
    return prompts

def main():
    path = '../prompts-generated/prompts.json'
    read_file = file_reader(path)
    print(json_parser(read_file))

main()