# automated_opt.py
"""
Simple automated prompt optimization via random hill-climb search.
Evaluates small changes in prompt templates and picks the best one.
"""

import random, copy
from utils import call_anthropic, DEFAULT_MODEL
from scoring import score_predictions
from prompts import BASE_PROMPT, ROLE_COT_PROMPT, FEW_SHOT_PROMPT

def build_prompt(question, config):
    """Builds a prompt version based on the configuration."""
    if config["style"] == "base":
        return BASE_PROMPT.format(question=question)
    elif config["style"] == "cot":
        return ROLE_COT_PROMPT.format(question=question)
    elif config["style"] == "few":
        return FEW_SHOT_PROMPT.format(question=question)
    else:
        return BASE_PROMPT.format(question=question)

def evaluate_config(config, sample, model=DEFAULT_MODEL, max_calls=10):
    """Evaluate prompt configuration on a small validation subset."""
    subset = random.sample(sample, min(max_calls, len(sample)))
    results = []
    for item in subset:
        q, gold = item["question"], item["answer"]
        prompt = build_prompt(q, config)
        try:
            reply = call_anthropic(prompt, model=model)
        except Exception as e:
            reply = f"ERROR: {e}"
        results.append({"prediction": reply, "gold": gold})
    acc = score_predictions(results)
    return acc

def hill_climb(sample, model=DEFAULT_MODEL, budget=10):
    """
    Performs a small random search over prompt variants.
    """
    space = [
        {"style": "base", "temperature": 0.0},
        {"style": "cot", "temperature": 0.0},
        {"style": "few", "temperature": 0.0},
        {"style": "cot", "temperature": 0.3},
        {"style": "few", "temperature": 0.3},
    ]
    best = {"config": None, "score": -1.0}
    for i in range(budget):
        cfg = random.choice(space)
        score = evaluate_config(cfg, sample, model)
        print(f"Trial {i+1}/{budget} — {cfg} => acc={score:.2f}")
        if score > best["score"]:
            best = {"config": cfg, "score": score}
    return best

