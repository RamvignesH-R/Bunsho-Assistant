from fastapi import FastAPI
from fastapi import BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
from threading import Lock

import os

from .processor import StreamProcessor
from .utils import (
    log_message,
    TRANSCRIPTS_DIR
)

# =========================================================
# APP
# =========================================================

app = FastAPI(
    title="FlowScribe Backend",
    version="3.0.0"
)

# =========================================================
# GLOBALS
# =========================================================

processors = {}

lock = Lock()

GLOBAL_KEYWORDS = [
    "vote",
    "motion",
    "objection",
    "bill passed",
    "adjourned"
]

SYSTEM_LOGS = []

# =========================================================
# HELPERS
# =========================================================

def add_log(message):

    SYSTEM_LOGS.append(message)

    if len(SYSTEM_LOGS) > 500:
        SYSTEM_LOGS.pop(0)

    log_message(message)

# =========================================================
# MODELS
# =========================================================

class KeywordAction(BaseModel):
    keyword: str

# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {
        "app": "FlowScribe",
        "status": "running"
    }

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

    with lock:

        if url in processors:

            return {
                "message": "Stream already active"
            }

        try:

            processor = StreamProcessor(
                url,
                source_type
            )

            processor.keywords = GLOBAL_KEYWORDS.copy()

            processors[url] = processor

            background_tasks.add_task(
                processor.start
            )

            add_log(
                f"Started stream: {url}"
            )

            return {
                "message": "Stream started successfully"
            }

        except Exception as e:

            add_log(
                f"Failed starting stream: {e}"
            )

            return {
                "message": f"Failed: {e}"
            }

# =========================================================
# STOP STREAM
# =========================================================

@app.post("/stop_stream")
def stop_stream(url: str):

    with lock:

        if url not in processors:

            return {
                "message": "Stream not found"
            }

        try:

            processors[url].stop()

            del processors[url]

            add_log(
                f"Stopped stream: {url}"
            )

            return {
                "message": "Stream stopped"
            }

        except Exception as e:

            add_log(
                f"Stop stream error: {e}"
            )

            return {
                "message": f"Error: {e}"
            }

# =========================================================
# STOP ALL
# =========================================================

@app.post("/stop_all")
def stop_all():

    with lock:

        count = 0

        for url in list(processors.keys()):

            try:

                processors[url].stop()

                del processors[url]

                count += 1

            except Exception as e:

                add_log(
                    f"Stop failed: {e}"
                )

        add_log(
            f"Stopped {count} streams"
        )

        return {
            "message": f"Stopped {count} streams"
        }

# =========================================================
# TRANSCRIPT
# =========================================================

@app.get("/transcript")
def transcript():

    all_lines = []
    alerts = []

    for proc in processors.values():

        all_lines.extend(
            proc.transcript_lines[-100:]
        )

        alerts.extend(
            proc.get_alerts()
        )

    return {
        "transcript": all_lines[-100:],
        "alerts": alerts[-20:]
    }

# =========================================================
# ACTIVE STREAMS
# =========================================================

@app.get("/streams")
def streams():

    data = []

    for url, proc in processors.items():

        data.append({
            "url": url,
            "type": proc.source_type,
            "status": "running"
        })

    return {
        "streams": data
    }

# =========================================================
# KEYWORDS
# =========================================================

@app.get("/keywords")
def keywords():

    return {
        "keywords": GLOBAL_KEYWORDS
    }

@app.post("/add_keyword")
def add_keyword(action: KeywordAction):

    keyword = action.keyword.lower().strip()

    if (
        keyword
        and keyword not in GLOBAL_KEYWORDS
    ):

        GLOBAL_KEYWORDS.append(keyword)

        for proc in processors.values():
            proc.add_keyword(keyword)

        add_log(
            f"Added keyword: {keyword}"
        )

    return {
        "message": f"Added keyword: {keyword}"
    }

@app.post("/remove_keyword")
def remove_keyword(action: KeywordAction):

    keyword = action.keyword.lower().strip()

    if keyword in GLOBAL_KEYWORDS:

        GLOBAL_KEYWORDS.remove(keyword)

        for proc in processors.values():
            proc.remove_keyword(keyword)

        add_log(
            f"Removed keyword: {keyword}"
        )

    return {
        "message": f"Removed keyword: {keyword}"
    }

# =========================================================
# SYSTEM LOGS
# =========================================================

@app.get("/logs")
def logs():

    return {
        "logs": SYSTEM_LOGS[-200:]
    }

# =========================================================
# TRANSCRIPT FILES
# =========================================================

@app.get("/transcript_files")
def transcript_files():

    files = []

    if os.path.exists(TRANSCRIPTS_DIR):

        for file in os.listdir(TRANSCRIPTS_DIR):

            if file.endswith(".txt"):

                files.append(file)

    return {
        "files": sorted(files, reverse=True)
    }

# =========================================================
# DOWNLOAD TRANSCRIPT
# =========================================================

@app.get("/download_transcript")
def download_transcript(filename: str):

    file_path = os.path.join(
        TRANSCRIPTS_DIR,
        filename
    )

    if not os.path.exists(file_path):

        return {
            "message": "File not found"
        }

    return FileResponse(
        file_path,
        media_type="text/plain",
        filename=filename
    )