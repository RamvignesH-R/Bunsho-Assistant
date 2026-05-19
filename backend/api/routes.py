import os
import tempfile

from fastapi import (
    APIRouter,
    UploadFile,
    File
)

from pydantic import BaseModel

from backend.services.ocr_service import (
    extract_text_from_image,
    extract_text_from_pdf
)

from backend.services.chat_service import (
    contract_chat
)

from backend.services.gemini_service import (
    analyze_contract
)

from backend.utils.text_cleaner import clean_japanese_ocr_text

router = APIRouter()


# =========================
# CHAT REQUEST MODEL
# =========================

class ChatRequest(BaseModel):
    document_text: str
    question: str
    history: list = []


# =========================
# ANALYZE DOCUMENT
# =========================

@router.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...)
):

    suffix = os.path.splitext(
        file.filename
    )[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as temp_file:

        content = await file.read()

        temp_file.write(content)

        temp_path = temp_file.name

    try:

        # =========================
        # OCR EXTRACTION
        # =========================

        if suffix.lower() == ".pdf":

            extracted_text = (
                extract_text_from_pdf(
                    temp_path
                )
            )

        else:

            extracted_text = (
                extract_text_from_image(
                    temp_path
                )
            )

        # =========================
        # PRE-CLEANING FOR TOKEN OPTIMIZATION
        # =========================
        # This acts similarly to RAG pre-processing step by eliminating OCR noise,
        # redundant spaces, and compressing full-width characters.
        
        cleaned_text = clean_japanese_ocr_text(extracted_text)

        # =========================
        # AI ANALYSIS
        # =========================

        analysis = analyze_contract(
            cleaned_text
        )

        return {

            "success": True,

            "filename": file.filename,

            "extracted_text":
                cleaned_text,

            "analysis": analysis
        }

    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)


# =========================
# CONTRACT CHAT
# =========================

@router.post("/chat")
async def ask_contract_question(
    payload: ChatRequest
):

    answer = contract_chat(
        payload.document_text,
        payload.question,
        payload.history
    )

    return {
        "answer": answer
    }