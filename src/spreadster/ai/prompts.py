def build_summary_prompt(payload: dict) -> str:
    return f"""
You are an options trading assistant.

Given:
1. the market regime
2. the gap/expected-move signal
3. the recommended strategy
4. the candidate trades with TOS code

Return:
- preferred strategy
- top 1 or 2 trades
- very brief explanation
- if confidence is low, say no trade

Payload:
{payload}
""".strip()
