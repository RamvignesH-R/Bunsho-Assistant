import os
import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def contract_chat(document_text, question, history=[]):

    history_str = ""
    for msg in history:
        role = "User" if msg.get("role") == "user" else "AI"
        history_str += f"{role}: {msg.get('text')}\n\n"

    prompt = f"""
You are a Japanese legal AI assistant.

DOCUMENT:

{document_text}

CHAT HISTORY:
{history_str}

USER QUESTION:

{question}

INSTRUCTIONS (SELF-RAG & REFLECTION FRAMEWORK):
1. [RETRIEVAL] Silently identify the exact clauses or sections from the DOCUMENT CONTEXT relevant to the USER QUESTION.
2. [COMPRESSION] Extract only the vital facts needed to answer.
3. [REFLECTION] Verify that your intended answer is 100% supported by the text. If the document does not contain the answer, explicitly state so and do not guess.
4. [GENERATION] Provide your final clear, simple answer in BOTH Japanese and English. Return it exactly as a raw JSON object with keys "japanese" and "english". Do not wrap in markdown blocks.

FORMAT:
{{
  "japanese": "...",
  "english": "..."
}}
"""

    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config=genai.GenerationConfig(
                temperature=0.2,
                response_mime_type="application/json",
            )
        )
        
        response = model.generate_content(prompt)
        content = response.text.strip()
        
        if content.startswith("```json"):
            content = content.replace("```json", "", 1)
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        try:
            import json
            return json.loads(content)
        except Exception:
            return {"english": content, "japanese": content}
    except Exception as e:
        return {"english": f"Error: {str(e)}", "japanese": f"Error: {str(e)}"}