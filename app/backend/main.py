from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import threading
import os

from .processor import StreamProcessor
from .utils import (
    log_message,
    LOGS_DIR,
    TRANSCRIPTS_DIR
)

# =========================================================
# APP
# =========================================================

app = FastAPI(
    title="FlowScribe Backend"
)

# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# GLOBALS
# =========================================================

processors = {}

lock = threading.Lock()

GLOBAL_KEYWORDS = [
    "vote",
    "motion",
    "objection",
    "bill passed",
    "adjourned"
]

# =========================================================
# MODELS
# =========================================================

class KeywordRequest(BaseModel):

    keyword: str

class StopStreamRequest(BaseModel):

    url: str

# =========================================================
# HEALTH
# =========================================================

@app.get("/health")

def health():

    return {
        "status": "online",
        "active_streams": len(processors),
        "keywords": len(GLOBAL_KEYWORDS)
    }

# =========================================================
# START STREAM
# =========================================================

@app.post("/start_stream")

async def start_stream(
    url: str,
    background_tasks: BackgroundTasks,
    source_type: str = "youtube"
):

    try:

        with lock:

            if url in processors:

                return {
                    "message": "stream already running"
                }

            processor = StreamProcessor(
                source_url=url,
                source_type=source_type
            )

            # sync keywords
            processor.keywords = GLOBAL_KEYWORDS.copy()

            processors[url] = processor

            background_tasks.add_task(
                processor.start
            )

            log_message(
                f"Started stream: {url}"
            )

        return {
            "message": "stream started"
        }

    except Exception as e:

        log_message(
            f"Failed to start stream: {e}"
        )

        return {
            "error": str(e)
        }

# =========================================================
# STOP STREAM
# =========================================================

@app.post("/stop_stream")

def stop_stream(request: StopStreamRequest):

    try:

        with lock:

            if request.url in processors:

                processors[request.url].stop()

                del processors[request.url]

                log_message(
                    f"Stopped stream: {request.url}"
                )

        return {
            "message": "stream stopped"
        }

    except Exception as e:

        return {
            "error": str(e)
        }

# =========================================================
# STOP ALL
# =========================================================

@app.post("/stop_all")

def stop_all():

    try:

        with lock:

            for url in list(processors.keys()):

                processors[url].stop()

                del processors[url]

            log_message(
                "Stopped all streams"
            )

        return {
            "message": "all streams stopped"
        }

    except Exception as e:

        return {
            "error": str(e)
        }

# =========================================================
# STREAMS
# =========================================================

@app.get("/streams")

def get_streams():

    stream_list = []

    for idx, (url, proc) in enumerate(processors.items()):

        stream_list.append({
            "id": idx + 1,
            "url": url,
            "type": proc.source_type,
            "running": proc.running,
            "transcript_count": len(proc.transcript_lines),
            "alert_count": len(proc.alerts)
        })

    return {
        "streams": stream_list
    }

# =========================================================
# TRANSCRIPTS
# =========================================================

@app.get("/transcript")

def get_transcript():

    all_lines = []
    all_alerts = []

    for proc in processors.values():

        all_lines.extend(
            proc.transcript_lines[-80:]
        )

        all_alerts.extend(
            proc.alerts[-20:]
        )

    return {
        "transcript": all_lines,
        "alerts": all_alerts
    }

# =========================================================
# LOGS
# =========================================================

@app.get("/logs")

def get_logs():

    log_file = os.path.join(
        LOGS_DIR,
        "system_log.txt"
    )

    if not os.path.exists(log_file):

        return {
            "logs": []
        }

    try:

        with open(
            log_file,
            "r",
            encoding="utf-8"
        ) as f:

            lines = f.readlines()

        return {
            "logs": [
                line.strip()
                for line in lines[-100:]
            ]
        }

    except Exception as e:

        return {
            "logs": [
                f"Failed to load logs: {e}"
            ]
        }

# =========================================================
# KEYWORDS
# =========================================================

@app.get("/keywords")

def get_keywords():

    return {
        "keywords": GLOBAL_KEYWORDS
    }

# =========================================================
# ADD KEYWORD
# =========================================================

@app.post("/add_keyword")

def add_keyword(request: KeywordRequest):

    keyword = request.keyword.lower().strip()

    if keyword not in GLOBAL_KEYWORDS:

        GLOBAL_KEYWORDS.append(keyword)

        for proc in processors.values():

            proc.add_keyword(keyword)

        log_message(
            f"Added keyword: {keyword}"
        )

    return {
        "message": "keyword added"
    }

# =========================================================
# REMOVE KEYWORD
# =========================================================

@app.post("/remove_keyword")

def remove_keyword(request: KeywordRequest):

    keyword = request.keyword.lower().strip()

    if keyword in GLOBAL_KEYWORDS:

        GLOBAL_KEYWORDS.remove(keyword)

        for proc in processors.values():

            proc.remove_keyword(keyword)

        log_message(
            f"Removed keyword: {keyword}"
        )

    return {
        "message": "keyword removed"
    }

# =========================================================
# TRANSCRIPT FILES
# =========================================================

@app.get("/transcript_files")

def transcript_files():

    try:

        files = sorted(
            os.listdir(TRANSCRIPTS_DIR),
            reverse=True
        )

        return {
            "files": files
        }

    except Exception as e:

        return {
            "files": [],
            "error": str(e)
        }