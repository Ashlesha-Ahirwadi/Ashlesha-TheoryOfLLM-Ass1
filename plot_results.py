# plot_results.py
import json
import matplotlib.pyplot as plt

with open("results/summary.json") as f:
    data = json.load(f)

labels = ["Baseline", "Role+CoT", "Few-shot", "Self-Consistency", "Meta", "Automated (best)"]
scores = [
    data["baseline_acc"],
    data["role_cot_acc"],
    data["few_shot_acc"],
    data["self_consistency_acc"],
    data["meta_acc"],
    data["automated_best"]["score"],
]

plt.figure(figsize=(8,5))
plt.bar(labels, scores)
plt.xticks(rotation=30, ha="right")
plt.ylabel("Accuracy")
plt.title("Prompt Engineering Performance Comparison (GSM8K)")
plt.tight_layout()
plt.show()
