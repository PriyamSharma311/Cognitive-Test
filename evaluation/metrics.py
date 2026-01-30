from sklearn.metrics import precision_score, recall_score, f1_score
from typing import Dict, List


def evaluate_predictions(
    y_true: List[int],
    y_pred: List[int]
) -> Dict[str, float]:
    """
    Generic evaluation metrics for classification tasks.
    Used for:
    - emotion detection
    - safety / risk detection
    """

    return {
        "precision": round(precision_score(y_true, y_pred, zero_division=0), 3),
        "recall": round(recall_score(y_true, y_pred, zero_division=0), 3),
        "f1": round(f1_score(y_true, y_pred, zero_division=0), 3)
    }


# ✅ Optional local test (NO Streamlit here)
if __name__ == "__main__":
    y_true = [1, 0, 1, 1, 0, 0]
    y_pred = [1, 0, 0, 1, 0, 1]

    metrics = evaluate_predictions(y_true, y_pred)
    print(metrics)
