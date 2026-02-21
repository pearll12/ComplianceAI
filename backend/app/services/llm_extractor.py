import os
import json
import re
import google.generativeai as genai

def _extract_json_object(text: str) -> dict:
    """
    Robustly extract the first JSON object from a model response.
    Handles markdown ```json blocks and extra commentary.
    """
    if not text:
        raise ValueError("Empty model response")

    # Remove ```json ... ``` wrappers if present
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    # Find first '{' and last '}' to isolate JSON object
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"Could not locate JSON object in response: {text[:200]}")

    json_str = text[start : end + 1]
    return json.loads(json_str)

def extract_rules_json_with_llm(policy_text: str) -> dict:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        # No key: return demo so pipeline keeps working
        return {
            "policy_name": "Demo Policy",
            "rules": [
                {
                    "rule_id": "R1",
                    "description": "Default-value transactions",
                    "field": "amount",
                    "operator": ">",
                    "threshold": 1000000,
                }
            ]
        }

    genai.configure(api_key=api_key)

    # Model name can be gemini-1.5-flash or gemini-1.5-pro
    model = genai.GenerativeModel("gemini-1.5-pro")

    prompt = f"""
You are a compliance rule extraction engine.

Extract compliance rules from the policy text below.

Return STRICT JSON ONLY (no markdown, no extra text).

Schema:
{{
  "policy_name": "string",
  "rules": [
    {{
      "rule_id": "R1",
      "description": "string",
      "field": "string | null",
      "operator": "> | >= | < | <= | == | != | null",
      "threshold": "number | null",
      "time_window_minutes": "number | null",
      "transaction_count_threshold": "number | null",
      "payment_methods": ["string"] ,
      "sender_bank_field": "string | null",
      "receiver_bank_field": "string | null"
    }}
  ]
}}

Policy text:
{policy_text}
""".strip()

    response = model.generate_content(prompt)

    # Different versions sometimes store output differently
    raw_text = getattr(response, "text", None)
    if not raw_text and hasattr(response, "candidates") and response.candidates:
        raw_text = response.candidates[0].content.parts[0].text

    # Debug print (TEMPORARY): helps you see what's going on
    print("\n--- GEMINI RAW OUTPUT START ---\n", raw_text, "\n--- GEMINI RAW OUTPUT END ---\n")

    try:
        return _extract_json_object(raw_text)
    except Exception as e:
        # If parsing failed, raise explicit error instead of silently fallback
        raise RuntimeError(f"Gemini returned non-JSON or malformed JSON. Error: {e}")