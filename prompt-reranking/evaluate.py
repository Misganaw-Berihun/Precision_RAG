import os
import sys
import json
import random

rpath = os.path.abspath('..')
if rpath not in sys.path:
    sys.path.insert(0, rpath)

from utility.read_file import file_reader, json_parser 
from elo_rating import calculate_elo
from montecarlo import get_montecarlo_score


def evaluate():
    path = '../prompts-generated/prompts.json'
    prompts_str = file_reader(path)
    prompts = json_parser(prompts_str)

    print(prompts)
    monte_carlo = get_montecarlo_score(prompts=prompts)
    elo = calculate_elo(prompts=prompts)

    result =  [{
        "prompt" : prompt,
        'Monte Carlo Evaluation': monte_carlo[prompt],
        'Elo Rating Evaluation': elo[prompt]
    } for prompt in prompts]

    return result

print(*evaluate())