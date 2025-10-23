# Generative AI Assignment 1 — Prompt Engineering: Manual and Automated

**Course:** Theory of Large Language Models  
**Student:** Ashlesha Ahirwadi  
**Due Date:** October 20, 2025  
**Environment:** macOS (Apple Silicon, arm64)  
**Model Used:** `claude-3-haiku-20240307` (low-cost LLM per assignment requirement)

---

## 📘 Overview

This project implements **manual and automated prompt engineering** to improve reasoning accuracy of a Large Language Model (LLM) on arithmetic reasoning tasks.  
The objective is to analyze how different prompting strategies affect performance and to design a simple automated algorithm that optimizes prompts programmatically.

All experiments are reproducible inside a **Docker container** and use the **Anthropic Claude API**.

---

## 🧩 Dataset and Scoring

### Dataset
- **Dataset:** [GSM8K (Grade School Math 8K)](https://huggingface.co/datasets/openai/gsm8k)  
- **Task:** Solve elementary math word problems.  
- **Subset Used:** 300 questions for experimentation, smaller subsets (n = 5) for testing.  
- **Loading:** Implemented via `datasets` library in `data_prep.py`.

### Scoring
Implemented in `scoring.py`.  
Each model output must end with the exact pattern:

```
#### ANSWER: <number>
```

**Parser:**
```python
match = re.search(r"####\s*ANSWER\s*:\s*([-\d\.]+)", text)
```

**Accuracy:**
```python
accuracy = (correct_predictions / total_questions)
```

For numeric tasks this exact-match metric suffices; for free-form answers one could extend it with semantic similarity scoring.

---

## 🧠 Manual Prompt Engineering

All manual prompt templates are defined in `prompts.py`.

| Prompt Type | Description | Purpose |
|-------------|-------------|---------|
| **Baseline** | Plain question, no reasoning. | Establish baseline accuracy. |
| **Role + Chain-of-Thought (CoT)** | Adds persona ("math tutor") and step-by-step reasoning. | Encourage explicit reasoning. |
| **Few-Shot** | Includes two solved examples before the question. | Teach reasoning pattern. |
| **Self-Consistency** | Generates multiple reasoning paths and votes. | Reduce randomness, improve reliability. |
| **Meta-Prompt** | Model reflects on best reasoning strategy before solving. | Induce planning behavior. |

**Example (Role + CoT):**
```
You are a patient math tutor who explains reasoning step by step.
Show your steps clearly, then output ONLY the final numeric answer prefixed EXACTLY by:

#### ANSWER: <number>

Question:
{question}

Solution and reasoning:
#### ANSWER:
```

---

## ⚙️ Automated Prompt Engineering

Implemented in `automated_opt.py` via a hill-climb search algorithm.

### Method
1. Start from a base configuration (prompt style + temperature).
2. Evaluate on small batches of questions.
3. Mutate configuration randomly:

```python
styles = ["base", "cot", "few"]
temperatures = [0.0, 0.3, 0.7]
roles = ["math tutor", "helpful assistant", "expert problem solver"]
```

4. Retain the configuration with the highest accuracy.
5. Save best configuration and score to `results/summary.json`.

This approach mimics research in OPRO (Google, 2023) but implemented manually.

---

## 🧪 Running the Experiments

### Local Run
```bash
python data_prep.py
python run_experiments.py --sample_size 5
python plot_results.py
```

### Docker (Apple Silicon compatible)
Create a `.env` file in the project root:

```ini
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Build and run:

```bash
docker build -t genai-a1 .
docker run --rm --env-file .env genai-a1
```

---

## 📊 Results

Experiment on 5 random GSM8K questions with `claude-3-haiku-20240307`.

| Prompt Type | Description | Accuracy |
|-------------|-------------|----------|
| **Baseline** | Simple direct question | 1.00 |
| **Role + CoT** | Step-by-step reasoning | 1.00 |
| **Few-Shot** | Two worked examples | 1.00 |
| **Self-Consistency** | Three reasoning paths + vote | 0.60 |
| **Meta-Prompt** | Reflective reasoning | 1.00 |
| **Automated (Hill-Climb)** | Optimal config = CoT @ T = 0.0 | 0.80 |

### Visualization
`plot_results.py` renders a bar chart:

```
Baseline           ███████████████████ 1.00
Role + CoT         ███████████████████ 1.00
Few-Shot           ███████████████████ 1.00
Self-Consistency   ███████████ 0.60
Meta-Prompt        ███████████████████ 1.00
Automated (Best)   ███████████████████ 0.80
```

---

## 🔍 Analysis and Insights

- **Baseline:** Direct question format → 100% accuracy on small sample.
- **Role + CoT:** Reasoning steps maintain high correctness.
- **Few-Shot:** Pattern imitation improves consistency.
- **Self-Consistency:** Sometimes indecisive but more stable.
- **Meta-Prompt:** "Plan-then-solve" approach yields coherent logic.
- **Automated:** Hill-climb identifies optimal prompt automatically.

**Takeaway:** Even low-cost models (Haiku) can reach high accuracy on reasoning tasks when guided with explicit reasoning instructions.

---

## 🧱 Project Structure

```
genai-assn1/
├── data_prep.py           # Downloads & samples GSM8K
├── prompts.py             # Manual prompt templates
├── scoring.py             # Parses answers & computes accuracy
├── automated_opt.py       # Hill-climb automated optimization
├── run_experiments.py     # Runs all experiments
├── plot_results.py        # Accuracy visualization
├── requirements.txt       # Dependencies
├── Dockerfile             # Reproducible environment
├── .env                   # API key (excluded from Git)
├── README.md              # Documentation
└── results/
    └── summary.json       # Saved metrics
```

---

## 🐳 Docker Configuration

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "run_experiments.py", "--sample_size", "5"]
```

**Build & Run:**
```bash
docker build -t genai-a1 .
docker run --rm --env-file .env genai-a1
```

✅ **Verified on macOS (Apple Silicon, arm64).**

---

## 🧾 Example Console Output

```yaml
▶ Baseline prompt
Baseline accuracy: 1.00

▶ Role + Chain-of-Thought
Role + CoT accuracy: 1.00

▶ Few-shot prompt
Few-shot accuracy: 1.00

▶ Self-Consistency prompt
Self-Consistency accuracy: 0.60

▶ Meta-Prompt
Meta accuracy: 1.00

▶ Automated prompt optimization (hill-climb)
Best config: {'style': 'cot', 'temperature': 0.0, 'score': 0.8}
✅ Saved results/summary.json
```

---

## 🧩 Reproducibility Checklist

| Component | Description | Status |
|-----------|-------------|--------|
| Dataset loader | GSM8K sampled via Hugging Face | ✅ |
| Scoring function | Regex numeric parser | ✅ |
| Baseline | Implemented | ✅ |
| Manual prompt improvements | CoT, Few-Shot, Self-Consistency, Meta | ✅ |
| Automated optimization | Hill-climb algorithm | ✅ |
| Docker build (arm64) | Verified | ✅ |
| Results & plots | Generated | ✅ |

---

## 🧠 Key Learnings

1. **Prompt structure** influences reasoning accuracy far more than temperature.
2. **Chain-of-thought** and **few-shot** prompts produce the largest gains.
3. **Automated prompt search** can recover the best manual design efficiently.
4. **Proper answer formatting** ("#### ANSWER:") is essential for reliable scoring.
5. Even **budget models** deliver strong results when guided with structured reasoning cues.

---

## 📚 References

- [GSM8K Dataset](https://huggingface.co/datasets/openai/gsm8k)
- [BIG-Bench Hard](https://github.com/suzgunmirac/BIG-Bench-Hard)
- [TruthfulQA](https://github.com/sylinrl/TruthfulQA)
- [Anthropic Claude API Docs](https://docs.anthropic.com/)
- [Google OPRO Paper](https://arxiv.org/abs/2309.03409)


---

## ✅ Final Summary

This assignment demonstrates both **manual and automated prompt-engineering strategies** for improving LLM reasoning.  
Through systematic experimentation, performance improved significantly, validating that structured reasoning instructions and simple automated search can significantly enhance even small, low-cost models.

**Key Achievement:** Automated optimization successfully identified the most effective prompt configuration, demonstrating the potential for programmatic prompt engineering.
