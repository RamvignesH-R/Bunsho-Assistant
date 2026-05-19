FROM python:3.12-slim

WORKDIR /app

# Install system dependencies required for OpenCV, Tesseract, and PaddleOCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-jpn \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set Tesseract path for Linux (override the Windows path in the code)
ENV TESSERACT_CMD="/usr/bin/tesseract"

# Copy requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code into a 'backend' subdirectory to preserve python import paths
COPY backend /app/backend

# Expose port
EXPOSE 8000

# Start FastAPI using Uvicorn with the correct module path
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
