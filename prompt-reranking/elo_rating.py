import random 

def elo_for_prompt(prompt, base_rating=1500, opponent_rating = 1600):
    outcomes = ['win', 'loss', 'draw']
    outcome = random.choice(outcomes)

    K = 30 
    R_base = 10 ** (base_rating / 400)
    R_opponent = 10 ** (opponent_rating/400)
    expected_score = R_base / (R_base + R_opponent)

    actual_score = {'win': 1, 'loss': 0, 'draw': 0.5}[outcome]
    new_rating = base_rating + K  * (actual_score - expected_score)

    return new_rating

def calculate_elo(prompts):
    elo_ratings = {prompt: 1500 for prompt in prompts}

    for _ in range(10):
        for prompt in prompts:
            elo_ratings[prompt] = elo_for_prompt(prompt, base_rating=elo_ratings[prompt])

    return elo_ratings