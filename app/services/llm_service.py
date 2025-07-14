import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def analyze_invoice_with_llm(extracted_fields: dict, full_text: str) -> dict:
    """
    Call OpenAI GPT model with extracted invoice fields and full text,
    to perform:
    - Field validation
    - Invoice summary generation
    - Risk/Anomaly detection
    """

    prompt = f"""
You are a financial invoice analysis assistant.

Here are the extracted fields from an invoice:
{extracted_fields}

The full text content of the invoice is:
{full_text}

Please help me with the following tasks:
1. Validate the extracted fields for correctness (e.g., date format, amount reasonableness).
2. Generate a brief summary of the invoice (2-3 sentences).
3. Identify any potential anomalies or risks found in the invoice.

Please respond in JSON format with the following keys:
- "validation": a dictionary with field names as keys and values as "ok" or an error description.
- "summary": a string containing the invoice summary.
- "risks": a list of strings describing any risks or anomalies, or an empty list if none.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=300,
    )

    content = response.choices[0].message.content.strip()

    import json

    try:
        result = json.loads(content)
    except Exception:
        # If JSON parsing fails, fallback to a simple response
        result = {
            "validation": {k: "ok" for k in extracted_fields.keys()},
            "summary": content,
            "risks": [],
        }
    return result
