from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.rule_engine import execute_policy, compute_metrics, load_rules, load_dataset
from app.api.policy import router as policy_router
import os

app = FastAPI(title="ComplianceAI", version="1.0")

# Allow your frontend (Vite default) to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "ComplianceAI backend running"}

@app.post("/run-demo")
def run_demo():
    print("\n🔥 Demo execution started...")
    BASE_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../")
    )

    DATA_PATH = os.path.join(BASE_DIR, "data", "HI-Small_Trans.csv")

    # 1. Load policy and dataset
    policy = load_rules("app/rules/latest_rules.json")
    df = load_dataset(DATA_PATH)

    # 2. Execute rules
    violations = execute_policy(policy["rules"], df)

    # 3. Compute metrics (if label exists)
    if "is_laundering" in df.columns:
        metrics = compute_metrics(df, violations)
    else:
        metrics = None

    return {
        "policy_name": policy["policy_name"],
        "total_transactions": len(df),
        "violations_found": len(violations),
        "metrics": metrics,
        "sample_violations": violations.head(5).to_dict(orient="records")
    }

# API routes
app.include_router(policy_router, prefix="/api")