import pandas as pd

def execute_threshold(rule: dict, df: pd.DataFrame) -> pd.Series:
    field = rule["field"]
    operator = rule["operator"]
    threshold = rule["threshold"]

    if field not in df.columns:
        raise ValueError(f"Field '{field}' not found in dataframe")

    if operator == ">":
        condition = df[field] > threshold
    elif operator == "<":
        condition = df[field] < threshold
    elif operator == ">=":
        condition = df[field] >= threshold
    elif operator == "<=":
        condition = df[field] <= threshold
    elif operator == "==":
        condition = df[field] == threshold
    elif operator == "!=":
        condition = df[field] != threshold
    else:
        raise ValueError(f"Unsupported operator '{operator}'")

    return condition.astype(int)