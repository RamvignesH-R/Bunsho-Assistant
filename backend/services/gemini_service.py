import os
import json
from pathlib import Path
import google.generativeai as genai

from dotenv import load_dotenv

# LOAD .env PROPERLY
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# GET API KEY
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print("GEMINI API KEY LOADED:", api_key[:10] if api_key else "NONE")

# SYSTEM PROMPT
SYSTEM_PROMPT = """
You are BureaucracyAI.

You are a Japanese Legal Risk Intelligence AI.

Your job:
- analyze Japanese legal/financial documents
- explain sections clearly
- detect hidden risks
- detect suspicious clauses
- detect penalties
- detect obligations
- guide users safely

RULES:

1. Use SIMPLE JAPANESE for all *_jp fields.

2. Use PROFESSIONAL ENGLISH for all *_en fields.

3. NEVER hallucinate fake risks.

4. If a category does not exist:
"この文書には該当する内容はありません。"

5. If informational only:
- risk_score = 0
- risk_level = "No Risk"

6. IMPORTANT:
japanese_summary MUST BE EXTREMELY LONG AND DETAILED.
Even if the document is a short 1-page form, you MUST elaborate heavily on:
- document sections and their legal implications
- step-by-step instructions on what the user must fill
- obligations and potential pitfalls
- good policies vs dangerous policies
- suspicious conditions and penalties
- risks before signing
DO NOT BE BRIEF. Expand on the context of the document extensively.

7. Focus on:
- fraud detection
- hidden traps
- renewal traps
- guarantor risks
- cancellation risks
- financial risks
- vague wording
- abusive conditions

8. Return VALID RAW JSON ONLY.

FORMAT:

{
  "risk_score": 0,
  "risk_level": "",

  "japanese_summary": "[Provide a massive summary. Detail what the document has as sections, what each section has, and what to fill if any. Explain what the agreement tells. List all good policies and conditions. List dangerous and fishy policies and conditions as bullets.]",
  "english_summary": "[Provide a massive summary. Detail what the document has as sections, what each section has, and what to fill if any. Explain what the agreement tells. List all good policies and conditions. List dangerous and fishy policies and conditions as bullets.]",

  "dangerous_clauses_jp": [],
  "dangerous_clauses_en": [],

  "financial_obligations_jp": [],
  "financial_obligations_en": [],

  "hidden_risks_jp": [],
  "hidden_risks_en": [],

  "consumer_advice_jp": [],
  "consumer_advice_en": [],

  "penalty_risks_jp": [],
  "penalty_risks_en": [],

  "cancellation_policies_jp": [],
  "cancellation_policies_en": [],

  "important_dates_jp": [],
  "important_dates_en": []
}
"""


def analyze_contract(text):

    try:

        # Using gemini-2.5-flash for massive 1 million token context window
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_PROMPT,
            generation_config=genai.GenerationConfig(
                temperature=0.3,
                response_mime_type="application/json",
            )
        )

        response = model.generate_content(f"DOCUMENT:\n{text}")
        cleaned = response.text.strip()

        if cleaned.startswith("```json"):
            cleaned = cleaned.replace("```json", "")
            cleaned = cleaned.replace("```", "")

        cleaned = cleaned.strip()

        # FIND FIRST JSON OBJECT ONLY
        start = cleaned.find("{")
        end = cleaned.rfind("}") + 1

        cleaned_json = cleaned[start:end]

        parsed = json.loads(cleaned_json, strict=False)

        return parsed

    except Exception as e:

        return {
            "risk_score": 0,
            "risk_level": "Unknown",
            "japanese_summary": f"Analysis failed: {str(e)}",
            "english_summary": f"Analysis failed: {str(e)}",
            "dangerous_clauses_en": [],
            "financial_obligations_en": [],
            "hidden_risks_en": [],
            "consumer_advice_en": [str(e)],
            "penalty_risks_en": [],
            "cancellation_policies_en": [],
            "important_dates_en": []
        }