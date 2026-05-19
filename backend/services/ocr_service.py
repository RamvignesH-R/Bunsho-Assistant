from paddleocr import PaddleOCR
import pytesseract
from PIL import Image
import cv2
import fitz
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# -----------------------------
# PaddleOCR Initialization
# -----------------------------

ocr = PaddleOCR(
    use_angle_cls=True,
    lang="japan"
)

# -----------------------------
# Tesseract Path
# -----------------------------

# Allow Docker environment variable to override Windows path
tess_cmd = os.getenv("TESSERACT_CMD", r"C:\Program Files\Tesseract-OCR\tesseract.exe")
pytesseract.pytesseract.tesseract_cmd = tess_cmd

# -----------------------------
# Image Preprocessing
# -----------------------------

def preprocess_image(image_path):

    image = cv2.imread(image_path)

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    denoised = cv2.fastNlMeansDenoising(gray)

    thresh = cv2.threshold(
        denoised,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    processed_path = image_path + "_processed.png"

    cv2.imwrite(processed_path, thresh)

    return processed_path

# -----------------------------
# PaddleOCR Extraction
# -----------------------------

def paddle_extract(image_path):

    result = ocr.ocr(image_path)

    extracted_lines = []

    for line in result:
        for item in line:

            text = item[1][0]

            confidence = item[1][1]

            extracted_lines.append({
                "text": text,
                "confidence": confidence
            })

    return extracted_lines

# -----------------------------
# Tesseract Verification
# -----------------------------

def tesseract_verify(image_path):

    image = Image.open(image_path)

    text = pytesseract.image_to_string(
        image,
        lang="jpn"
    )

    return text

# -----------------------------
# Single Image OCR Pipeline
# -----------------------------

def process_single_image(image_path):

    processed_path = preprocess_image(image_path)

    paddle_result = paddle_extract(processed_path)

    final_lines = []

    for item in paddle_result:

        text = item["text"]

        confidence = item["confidence"]

        # low confidence → verify with tesseract

        if confidence < 0.80:

            verified_text = tesseract_verify(
                processed_path
            )

            if verified_text.strip():
                final_lines.append(
                    verified_text.strip()
                )
            else:
                final_lines.append(text)

        else:
            final_lines.append(text)

    try:
        os.remove(processed_path)
    except:
        pass

    return "\n".join(final_lines)

# -----------------------------
# PDF OCR Pipeline
# -----------------------------

def extract_text_from_pdf(pdf_path):

    document = fitz.open(pdf_path)

    full_text = []

    for page_number in range(len(document)):

        page = document.load_page(page_number)

        pix = page.get_pixmap(dpi=300)

        image_path = (
            f"{pdf_path}_page_{page_number}.png"
        )

        pix.save(image_path)

        page_text = process_single_image(
            image_path
        )

        full_text.append(page_text)

        try:
            os.remove(image_path)
        except:
            pass

    return "\n".join(full_text)

# -----------------------------
# Main Extraction Entry
# -----------------------------

def extract_japanese_text(file_path):

    extension = (
        file_path
        .lower()
        .split(".")[-1]
    )

    if extension == "pdf":
        return extract_text_from_pdf(file_path)

    return process_single_image(file_path)

# compatibility wrapper

def extract_text_from_image(file_path):
    return process_single_image(file_path)