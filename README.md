---
title: Bunsho Assistant API
emoji: 🛡️
colorFrom: blue
colorTo: blue
sdk: docker
app_port: 8000
---

<div align="center">
  <img src="https://img.shields.io/badge/Next.js-black?style=for-the-badge&logo=next.js&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/Gemini_2.5_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white" />
  <img src="https://img.shields.io/badge/PaddleOCR-blue?style=for-the-badge&logo=python" />
</div>

<h1 align="center">🛡️ Bunsho Assistant (formerly BureaucracyAI)</h1>

**Bunsho Assistant** is an advanced, AI-powered legal document analyzer designed specifically for processing complex Japanese bureaucratic and legal documents. It automatically extracts text via OCR, analyzes potential risks using Google Gemini's massive context window, and provides detailed, structured reports in both English and Japanese.

---

## 🌟 Live Demo

Don't want to deal with local setup and massive ML models? Use our free, cloud-hosted version!
- **Frontend (UI):** [https://bunsho-assistant-flax.vercel.app](https://bunsho-assistant-flax.vercel.app) 
- **Backend API:** [https://ramvicky2004-bunsho-assistant-api.hf.space](https://ramvicky2004-bunsho-assistant-api.hf.space)

---

## ✨ Features

- **Advanced OCR Pipeline:** Utilizes `PaddleOCR` and `Tesseract` to accurately extract Japanese text from dense PDFs and images.
- **Deep Legal Analysis:** Powered by `Google Gemini 2.5 Flash`, the system flags dangerous clauses, financial obligations, hidden risks, and cancellation penalties.
- **Global Language Toggle:** Instantly switch between English and Japanese UI/Analysis with a seamless global state architecture.
- **Interactive Document Chat:** Ask specific questions about your uploaded document directly to the AI.
- **Printable PDF Reports:** Generate clean, structured PDF reports detailing the risk score and findings.

---

## 🏗️ Architecture

This project was built to prevent Out-Of-Memory (OOM) crashes caused by heavy Machine Learning models, utilizing a robust split-stack architecture:

1. **Frontend (Vercel):** A Next.js application styled with TailwindCSS and Lucide-React icons, providing a dynamic, glassmorphism-inspired user interface.
2. **Backend (Hugging Face Spaces):** A FastAPI server running in a custom Docker container. Hosted on Hugging Face Spaces to provide the required 16GB of RAM needed to comfortably run PaddleOCR without crashing.

---

## 💻 Local Development Setup

If you wish to run this heavy architecture locally, follow these precise steps.

### Prerequisites
- Python 3.12+
- Node.js 18+
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) installed on your machine (`tesseract-ocr-jpn` required).

### 1. Backend Setup (FastAPI + AI)

```bash
cd backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install heavy ML dependencies
pip install -r requirements.txt

# Environment Variables
# Create a .env file in the backend directory:
# GEMINI_API_KEY=your_google_ai_studio_key_here

# Start the API
uvicorn backend.main:app --reload
```
*The backend will run on `http://127.0.0.1:8000`.*

### 2. Frontend Setup (Next.js)

```bash
cd frontend

# Install UI dependencies
npm install

# Start the development server
npm run dev
```
*The frontend will run on `http://localhost:3000`.*

---

## 🐳 Docker Deployment

The repository includes a highly optimized Linux `Dockerfile` at the root directory specifically designed for Hugging Face Spaces. It automatically installs system-level dependencies (`libgl1`, `poppler-utils`, `tesseract-ocr-jpn`) before booting the FastAPI server.

To deploy on Hugging Face Spaces:
1. Create a new Docker Space.
2. Set hardware to `Free (2 vCPU, 16GB RAM)`.
3. Push this repository to the Space.
4. Add `GEMINI_API_KEY` to the Space Secrets.

---
*Built with ❤️ to navigate Japanese bureaucracy safely and intelligently.*
