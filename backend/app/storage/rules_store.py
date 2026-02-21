import json
from pathlib import Path

RULES_DIR = Path(__file__).resolve().parents[1] / "rules"
RULES_FILE = RULES_DIR / "latest_rules.json"

def save_rules_json(data: dict) -> None:
    RULES_DIR.mkdir(parents=True, exist_ok=True)
    RULES_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

def load_rules_json() -> dict:
    if not RULES_FILE.exists():
        return {"policy_name": "None", "rules": []}
    return json.loads(RULES_FILE.read_text(encoding="utf-8"))