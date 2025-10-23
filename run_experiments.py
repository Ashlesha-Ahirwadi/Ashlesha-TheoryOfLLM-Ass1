# run_experiments.py
import os, json, argparse
from tqdm import tqdm
from dotenv import load_dotenv
from scoring import score_predictions
from data_prep import download_gsm8k, sample_questions
from prompts import (
    BASE_PROMPT,
    ROLE_COT_PROMPT,
    FEW_SHOT_PROMPT,
    SELF_CONSISTENCY_PROMPT,
    META_PROMPT,
)
from anthropic import Anthropic

load_dotenv()

def call_claude(prompt, model="claude-3-haiku-20240307", temperature=0.3):
    """
    Call Anthropic Claude with retry and error handling.
    """
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    try:
        response = client.messages.create(
            model=model,
            max_tokens=500,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
    except Exception as e:
        print(f"--- Claude raw output ---\nERROR: {e}\n---------------------------")
        return ""

def evaluate_prompt(items, template, model, label):
    results = []
    print(f"\n▶ {label}")
    for q in tqdm(items):
        question = q["question"]
        gold = q["answer"].split("####")[-1].strip() if "####" in q["answer"] else q["answer"]
        prompt = template.format(question=question)
        text = call_claude(prompt, model=model)
        results.append({"prediction": text, "gold": gold})
    acc = score_predictions(results)
    print(f"{label} accuracy: {acc:.2f}")
    return acc

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample_size", type=int, default=5)
    parser.add_argument("--model", type=str, default="claude-3-haiku-20240307")
    args = parser.parse_args()

    ds = download_gsm8k()
    items = sample_questions(ds, n=args.sample_size)

    # Baseline
    base_acc = evaluate_prompt(items, BASE_PROMPT, args.model, "Baseline prompt")

    # Role + Chain-of-Thought
    cot_acc = evaluate_prompt(items, ROLE_COT_PROMPT, args.model, "Role + Chain-of-Thought")

    # Few-shot
    fs_acc = evaluate_prompt(items, FEW_SHOT_PROMPT, args.model, "Few-shot prompt")

    # Self-consistency
    sc_acc = evaluate_prompt(items, SELF_CONSISTENCY_PROMPT, args.model, "Self-Consistency prompt")

    # Meta-prompt
    meta_acc = evaluate_prompt(items, META_PROMPT, args.model, "Meta-Prompt")

    # Automated optimization (hill-climb)
    print("\n▶ Automated prompt optimization (hill-climb)")
    from automated_opt import hill_climb
    best = hill_climb(items, args.model, budget=5)
    print(f"Best config: {best}")

    summary = {
        "baseline_acc": base_acc,
        "role_cot_acc": cot_acc,
        "few_shot_acc": fs_acc,
        "self_consistency_acc": sc_acc,
        "meta_acc": meta_acc,
        "automated_best": best,
    }

    os.makedirs("results", exist_ok=True)
    with open("results/summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print("\n✅ Saved results/summary.json")

if __name__ == "__main__":
    main()
