import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, f1_score


def compute_comprehension_improvement(baseline_df, ai_df):
    """
    Compare baseline comprehension vs AI-assisted comprehension.

    baseline_df: DataFrame with baseline scores
    ai_df: DataFrame with AI-assisted scores

    Both must contain:
    - child_id
    - comprehension_score (0–100)
    """

    merged = pd.merge(
        baseline_df,
        ai_df,
        on="child_id",
        suffixes=("_baseline", "_ai")
    )

    merged["improvement"] = (
        merged["comprehension_score_ai"]
        - merged["comprehension_score_baseline"]
    )

    avg_improvement = merged["improvement"].mean()

    return {
        "average_improvement": round(avg_improvement, 2),
        "per_child": merged[["child_id", "improvement"]]
    }


def classify_understanding(score, threshold=60):
    """
    Convert comprehension score into binary understanding label.
    """
    return 1 if score >= threshold else 0


def compute_understanding_accuracy(baseline_df, ai_df):
    """
    Evaluate how well AI responses align with expected comprehension.

    baseline_df:
      - child_id
      - comprehension_score

    ai_df:
      - child_id
      - predicted_score
    """

    merged = pd.merge(
        baseline_df,
        ai_df,
        on="child_id",
        suffixes=("_baseline", "_ai")
    )

    # Use baseline comprehension as ground truth
    y_true = merged["comprehension_score_baseline"].apply(classify_understanding)
    y_pred = merged["predicted_score"].apply(classify_understanding)

    accuracy = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    return {
        "accuracy": round(accuracy, 3),
        "f1_score": round(f1, 3)
    }



# ---------- Quick test ----------
if __name__ == "__main__":
    baseline = pd.DataFrame({
        "child_id": [1, 2, 3],
        "comprehension_score": [45, 60, 50]
    })

    ai = pd.DataFrame({
        "child_id": [1, 2, 3],
        "comprehension_score": [65, 75, 70],
        "predicted_score": [70, 80, 75]
    })

    print(compute_comprehension_improvement(baseline, ai))
    print(compute_understanding_accuracy(baseline, ai))
