import re
import unicodedata

def clean_japanese_ocr_text(text: str) -> str:
    """
    Cleans OCR-extracted Japanese text to drastically reduce token count 
    for LLM consumption without losing legal meaning.
    """
    if not text:
        return ""

    # 1. Normalize Unicode (converts full-width alphanumeric to half-width, normalizes spaces)
    # This reduces token count by standardizing characters.
    text = unicodedata.normalize('NFKC', text)

    # 2. Split into lines to process line-by-line
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        
        # Skip completely empty lines
        if not line:
            continue
            
        # Optional: Skip extremely short OCR noise lines (e.g., stray single letters like "P" or "|")
        # Keep if it contains digits (like "1." or page numbers "12") or Japanese characters.
        if len(line) == 1 and not line.isalnum():
            continue
            
        # 3. Reduce multiple spaces to a single space
        line = re.sub(r'[ \t]+', ' ', line)
        
        # 4. Remove spaces specifically around Japanese punctuation to save tokens
        line = re.sub(r' ([、。！？「」『』（）［］])', r'\1', line)
        line = re.sub(r'([、。！？「」『』（）［］]) ', r'\1', line)
        
        # 5. Remove spaces between Japanese Kanji/Hiragana/Katakana characters
        # OCR often hallucinates spaces like "契 約 書" -> "契約書"
        # Regex explanation: (?<=[^\x00-\x7F]) (?=[^\x00-\x7F]) matches a space between two non-ASCII characters
        line = re.sub(r'(?<=[^\x00-\x7F]) (?=[^\x00-\x7F])', '', line)
        
        cleaned_lines.append(line)

    # Join lines back together
    cleaned_text = '\n'.join(cleaned_lines)
    
    return cleaned_text
