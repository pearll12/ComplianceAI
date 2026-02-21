# rule_engine/metrics.py

from sklearn.metrics import precision_score, recall_score, f1_score
import numpy as np

def compute_metrics(df, violations):
    print("\n📊 Computing evaluation metrics...")

    if "is_laundering" not in df.columns:
        raise ValueError("❌ Dataset must contain 'is_laundering' column")

    # Ground truth
    y_true = df["is_laundering"].values

    # Build prediction array (same length as dataset)
    y_pred = np.zeros(len(df))

    # Mark flagged rows as predicted suspicious
    y_pred[violations.index] = 1

    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")

    return {
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }