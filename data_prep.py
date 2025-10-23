# data_prep.py
from datasets import load_dataset
import random
import json

def download_gsm8k(cache_dir=None):
    """
    Downloads the GSM8K dataset from Hugging Face.
    """
    ds = load_dataset("openai/gsm8k", "main", cache_dir=cache_dir)
    return ds["train"]

def sample_questions(dataset, n=300, seed=42, out_path=None):
    random.seed(seed)
    idx = list(range(len(dataset)))
    random.shuffle(idx)
    idx = idx[:n]
    selected = [dataset[i] for i in idx]
    if out_path:
        with open(out_path, "w") as f:
            json.dump(selected, f, indent=2)
    return selected

if __name__ == "__main__":
    ds = download_gsm8k()
    sample_questions(ds, n=10, out_path="sample_gsm8k.json")
    print("✅ Saved sample_gsm8k.json")

