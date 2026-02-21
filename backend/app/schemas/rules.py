from pydantic import BaseModel, Field
from typing import List, Optional, Literal

Operator = Literal[">", ">=", "<", "<=", "==", "!="]

class Rule(BaseModel):
    rule_id: str = Field(..., examples=["R1"])
    description: str

    # basic rule type
    field: Optional[str] = None
    operator: Optional[Operator] = None
    threshold: Optional[float] = None

    # for time-window rules
    time_window_minutes: Optional[int] = None
    transaction_count_threshold: Optional[int] = None

    # for categorical rules (like CASH/CHEQUE)
    payment_methods: Optional[List[str]] = None

    # for cross-bank transfer
    sender_bank_field: Optional[str] = None
    receiver_bank_field: Optional[str] = None

class PolicyRules(BaseModel):
    policy_name: str = "Policy"
    rules: List[Rule]