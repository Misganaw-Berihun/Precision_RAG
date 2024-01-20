from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict

app = FastAPI()

def generate_prompts(description: str, scenarios: List[str], expected_outputs: List[str]) -> List[str]:
    return [f"{description} {scenario} {expected_output}" for scenario, expected_output in zip(scenarios, expected_outputs)]

def evaluate_prompt(description: str, generated_prompt: str) -> float:
    return abs(len(description) - len(generated_prompt))

def generate_evaluation_data(description: str, scenarios: List[str], expected_outputs: List[str]) -> List[Dict[str, float]]:
    evaluation_data = []
    for scenario, expected_output in zip(scenarios, expected_outputs):
        generated_prompt = generate_prompts(description, [scenario], [expected_output])[0]
        evaluation_score = evaluate_prompt(description, generated_prompt)
        evaluation_data.append({"prompt": generated_prompt, "evaluation_score": evaluation_score})
    return evaluation_data

@app.post("/generate_prompts")
def generate_prompts_api(description: str, scenarios: List[str], expected_outputs: List[str]):
    prompts = generate_prompts(description, scenarios, expected_outputs)
    return {"prompts": prompts}

@app.post("/evaluate_prompt")
def evaluate_prompt_api(description: str, generated_prompt: str):
    evaluation_score = evaluate_prompt(description, generated_prompt)
    return {"evaluation_score": evaluation_score}

@app.post("/generate_evaluation_data")
def generate_evaluation_data_api(description: str, scenarios: List[str], expected_outputs: List[str]):
    evaluation_data = generate_evaluation_data(description, scenarios, expected_outputs)
    return {"evaluation_data": evaluation_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
