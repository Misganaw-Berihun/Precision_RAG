import random

def monte_carlo_eval(prompt):
    resposne_types = ['highly_relevant', 'somewhat relevant', 'irrelevant']
    scores = {'highly_relevant': 3, 'somewhat relevant': 2, 'irrelevant': 1}

    trials = 100
    total_score = 0

    for _ in range(trials):
        response = random.choice(resposne_types)
        total_score += scores[response]
    
    return total_score / scores[response]


def get_montecarlo_score(prompts):

    monte_evaluations = {}
    for prompt in prompts:
        monte_evaluations[prompt] = monte_carlo_eval(prompt=prompt)
    
    return monte_evaluations
