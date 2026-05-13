FROM python:3.10-slim

# =========================================================
# ENVIRONMENT
# =========================================================

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# =========================================================
# WORKDIR
# =========================================================

WORKDIR /app

# =========================================================
# SYSTEM PACKAGES
# =========================================================

RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    curl \
    wget \
    gcc \
    g++ \
    build-essential \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# =========================================================
# PYTHON DEPENDENCIES
# =========================================================

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

# =========================================================
# COPY PROJECT
# =========================================================

COPY . .

# =========================================================
# REQUIRED FOLDERS
# =========================================================

RUN mkdir -p product_created/transcripts
RUN mkdir -p product_created/logs

# =========================================================
# EXPOSE
# =========================================================

EXPOSE 7860

# =========================================================
# START SERVICES
# =========================================================

CMD bash -c "\
uvicorn app.backend.main:app \
--host 0.0.0.0 \
--port 9000 & \
streamlit run app/frontend/dashboard.py \
--server.port 7860 \
--server.address 0.0.0.0 \
--server.headless true"