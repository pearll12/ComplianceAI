# rule_engine/loader.py
import os
import json
import pandas as pd

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

DATA_PATH = os.path.join(BASE_DIR, "data", "HI-Small_Trans.csv")

def load_rules(path="rules/latest_rules.json"):
    print("📦 Loading rules...")
    with open(path, "r") as f:
        return json.load(f)

def load_dataset(path=DATA_PATH):
    print("📊 Loading dataset...")
    df = pd.read_csv(path)

    if "transaction_time" in df.columns:
        df["transaction_time"] = pd.to_datetime(df["transaction_time"])

    print("✅ Dataset loaded:", len(df), "rows")
    return df

if __name__ == "__main__":
    print("🔎 Testing loader...")

    df = load_dataset()
    print(df.head())

    # Optional: test rules too
    # rules = load_rules()
    # print(rules)