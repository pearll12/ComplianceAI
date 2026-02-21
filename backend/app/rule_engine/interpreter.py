import json
import pandas as pd
import operator

OPERATOR_MAP = {
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
    "==": operator.eq,
    "!=": operator.ne,
}

# Field mapping from logical names in rules → actual CSV columns
FIELD_MAP = {
    "transaction_time": "Timestamp",
    "amount": "Amount Paid",           # use Amount Received if needed
    "sender_bank_field": "From Bank",
    "receiver_bank_field": "To Bank",
    "account_id": "From Account",      # or To Account depending on use case
    "payment_method": "Payment Format",
    "field":""

}

def map_field(field):
    """Map rule field to actual CSV column, return None if missing"""
    if field in FIELD_MAP:
        return FIELD_MAP[field] or None
    return field if field else None

def apply_threshold_rule(rule, df):
    print(f"\n🔎 Executing Rule {rule.get('rule_id', 'Unknown')} (Threshold Rule)")

    # map field and skip if None
    field = map_field(rule.get("field"))
    if not field or field not in df.columns:
        print(f"⚠️ Skipping rule {rule.get('rule_id')} - field is missing or None")
        return pd.DataFrame()  # empty, so it won't append

    operator_symbol = rule.get("operator")
    threshold = rule.get("threshold")

    op_func = OPERATOR_MAP.get(operator_symbol)
    if operator_symbol is not None and not op_func:
        print(f"⚠️ Skipping rule {rule.get('rule_id')} - unsupported operator {operator_symbol}")
        return pd.DataFrame()

    mask = op_func(df[field], threshold)
    flagged = df[mask].copy()
    flagged["triggered_rule"] = rule.get("rule_id", "Unknown")

    print("🚩 Violations found:", len(flagged))
    return flagged

# def apply_cross_bank_rule(rule, df):
#     print(f"\n🔎 Executing Rule {rule['rule_id']} (Cross-Bank Rule)")

#     # Map rule fields → actual CSV columns
#     sender_field = map_field(rule["sender_bank_field"])
#     receiver_field = map_field(rule["receiver_bank_field"])

#     if sender_field not in df.columns or receiver_field not in df.columns:
#         raise ValueError(f"❌ Sender ({sender_field}) or receiver ({receiver_field}) bank field missing")

#     mask = df[sender_field] != df[receiver_field]

#     flagged = df[mask].copy()
#     flagged["triggered_rule"] = rule["rule_id"]

#     print("🚩 Cross-bank transactions:", len(flagged))
#     return flagged

def apply_frequency_rule(rule, df):
    # Check for required fields in rule
    required_rule_fields = ["time_window_minutes", "transaction_count_threshold"]
    if any(rule.get(f) is None for f in required_rule_fields):
        print(f"⚠️ Skipping Rule {rule.get('rule_id')} due to missing rule parameters")
        return pd.DataFrame()

    print(f"\n🔎 Executing Rule {rule['rule_id']} (Frequency Rule)")
    time_window = rule["time_window_minutes"]
    txn_threshold = rule["transaction_count_threshold"]

    account_field = map_field("account_id")
    txn_amount_field = map_field("amount")
    time_field = map_field("transaction_time")

    # Check that these fields exist in the dataframe
    for f in [account_field, txn_amount_field, time_field]:
        if f not in df.columns:
            print(f"⚠️ Skipping Rule {rule.get('rule_id')} because field '{f}' is missing in dataset")
            return pd.DataFrame()

    # Convert timestamp column to datetime, drop invalid timestamps
    df_sorted = df.copy()
    df_sorted[time_field] = pd.to_datetime(df_sorted[time_field], errors='coerce')
    df_sorted = df_sorted.dropna(subset=[time_field])

    df_sorted = df_sorted.sort_values(time_field)
    flagged_indices = []

    # Group by account
    for account, group in df_sorted.groupby(account_field):
        group = group.set_index(time_field)
        rolling_counts = group[txn_amount_field].rolling(f"{time_window}min").count()
        suspicious = rolling_counts > txn_threshold
        flagged_indices.extend(group[suspicious].index)

    flagged = df_sorted[df_sorted[time_field].isin(flagged_indices)].copy()
    flagged["triggered_rule"] = rule["rule_id"]

    print("🚩 High-frequency violations:", len(flagged))
    return flagged

def apply_payment_method_rule(rule, df):
    print(f"\n🔎 Executing Rule {rule['rule_id']} (Payment Method Rule)")
    methods = rule["payment_methods"]
    threshold = rule.get("threshold", 0)

    payment_field = map_field("payment_method")
    amount_field = map_field("amount")

    if payment_field not in df.columns:
        raise ValueError(f"❌ {payment_field} column missing")

    mask = df[payment_field].isin(methods) & (df[amount_field] > threshold)
    flagged = df[mask].copy()
    flagged["triggered_rule"] = rule["rule_id"]

    print("🚩 High-risk payment violations:", len(flagged))
    return flagged

def execute_policy(rules, df):
    print("\n🚀 Starting policy execution...\n")
    all_violations = []

    for rule in rules:
        # Decide rule type based on JSON structure
        if rule.get("time_window_minutes") is not None:
            result = apply_frequency_rule(rule, df)
        # elif rule.get("sender_bank_field") is not None:
            # result = apply_cross_bank_rule(rule, df)
        elif rule.get("payment_methods"):
            result = apply_payment_method_rule(rule, df)
        else:
            result = apply_threshold_rule(rule, df)

        if not result.empty:
            all_violations.append(result)

    if not all_violations:
        print("✅ No violations found.")
        return pd.DataFrame()

    combined = pd.concat(all_violations, ignore_index=True)
    print("\n📌 Total violations across all rules:", len(combined))
    return combined