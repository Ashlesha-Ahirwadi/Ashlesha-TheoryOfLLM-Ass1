# scoring.py (improved version)
import re

def parse_answer(text):
    """Extracts numeric answer from text."""
    if not text:
        return None
    # Prefer the #### ANSWER pattern
    m = re.search(r"####\s*ANSWER\s*[:\-]?\s*([-\d\.]+)", text)
    if m:
        return m.group(1).strip()
    # fallback: take last number in text
    nums = re.findall(r"-?\d+\.?\d*", text)
    return nums[-1] if nums else None

def is_numeric_equal(pred, gold, tol=1e-6):
    """Compare two numbers within tolerance."""
    try:
        return abs(float(pred) - float(gold)) <= tol
    except:
        try:
            return int(pred) == int(gold)
        except:
            return False

def score_predictions(results):
    """Compute accuracy over predictions."""
    correct, total = 0, len(results)
    for r in results:
        pred = parse_answer(r.get("prediction", ""))
        gold = parse_answer(r.get("gold", ""))
        if pred is not None and gold is not None and is_numeric_equal(pred, gold):
            correct += 1
    return correct / total if total else 0.0

if __name__ == "__main__":
    # test
    test = [
        {"prediction": "#### ANSWER: 12", "gold": "12 + 3 = 15 #### 15"},
        {"prediction": "Answer: 9", "gold": "9"},
        {"prediction": "It's 7.", "gold": "7"},
    ]
    acc = score_predictions(test)
    print(f"✅ Test accuracy: {acc:.2f}")

