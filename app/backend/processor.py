import os
import time
import threading
import subprocess
import numpy as np
import soundfile as sf
import ffmpeg
import torch

from faster_whisper import WhisperModel
from pyannote.audio import Pipeline
from dotenv import load_dotenv

from .utils import (
    log_message,
    TRANSCRIPTS_DIR,
    get_session_filename
)

load_dotenv()

# =========================================================
# GLOBAL SHARED MODELS
# =========================================================

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

log_message(f"Loading Whisper model on {DEVICE}...")

WHISPER_MODEL = WhisperModel(
    "base",
    device=DEVICE,
    compute_type="float16" if DEVICE == "cuda" else "int8"
)

log_message("Whisper model loaded successfully")

HF_TOKEN = os.getenv("HF_TOKEN")

DIARIZATION_PIPELINE = None

if HF_TOKEN:
    try:
        log_message("Loading pyannote diarization pipeline...")

        DIARIZATION_PIPELINE = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            token=HF_TOKEN
        )

        if DEVICE == "cuda":
            DIARIZATION_PIPELINE.to(torch.device("cuda"))

        log_message("Pyannote diarization loaded")

    except Exception as e:
        log_message(f"Failed to load diarization pipeline: {e}")

# =========================================================
# STREAM PROCESSOR
# =========================================================

class StreamProcessor:

    def __init__(self, source_url, source_type="youtube"):

        self.source_url = source_url
        self.source_type = source_type.lower()

        self.running = False
        self.thread = None

        self.transcript_lines = []
        self.alerts = []

        self.keywords = [
            "vote",
            "motion",
            "objection",
            "bill passed",
            "adjourned"
        ]

        self.full_audio = []

        self.transcript_file = os.path.join(
            TRANSCRIPTS_DIR,
            get_session_filename()
        )

        log_message(
            f"Processor initialized: {self.source_url}"
        )

    # =====================================================
    # START
    # =====================================================

    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self._process_loop,
            daemon=True
        )

        self.thread.start()

        log_message(f"Started stream: {self.source_url}")

    # =====================================================
    # STOP
    # =====================================================

    def stop(self):

        self.running = False

        if self.thread:
            self.thread.join(timeout=10)

        self._run_diarization()

        self._save_transcript()

        log_message(f"Stopped stream: {self.source_url}")

    # =====================================================
    # MAIN PROCESS LOOP
    # =====================================================

    def _process_loop(self):

        try:

            audio_gen, sr = self._get_audio_stream()

            chunk_duration = 3
            samples_per_chunk = sr * chunk_duration

            buffer = np.array([], dtype=np.float32)

            for raw_chunk in audio_gen:

                if not self.running:
                    break

                buffer = np.append(buffer, raw_chunk)

                while len(buffer) >= samples_per_chunk:

                    chunk = buffer[:samples_per_chunk]
                    buffer = buffer[samples_per_chunk:]

                    self.full_audio.extend(chunk)

                    segments, _ = WHISPER_MODEL.transcribe(
                        chunk,
                        language="en",
                        beam_size=5,
                        vad_filter=True,
                        vad_parameters=dict(
                            min_silence_duration_ms=500
                        )
                    )

                    timestamp = time.strftime("%H:%M:%S")

                    for seg in segments:

                        text = seg.text.strip()

                        if not text:
                            continue

                        line = f"[{timestamp}] Speaker ?: {text}"

                        self.transcript_lines.append(line)

                        # ─── auto-save every 10 lines ───
                        if len(self.transcript_lines) % 10 == 0:
                            self._save_transcript()

                        lower_text = text.lower()

                        for kw in self.keywords:

                            if kw in lower_text:

                                alert = (
                                    f"ALERT: '{kw}' detected "
                                    f"at {timestamp}"
                                )

                                self.alerts.append(alert)

                                log_message(alert)

                    time.sleep(0.05)

        except Exception as e:

            log_message(f"Processing error: {e}")

        finally:

            self.running = False

    # =====================================================
    # AUDIO STREAM
    # =====================================================

    def _get_audio_stream(self):

        sr = 16000

        if self.source_type == "youtube":

            # ── iOS client trick bypasses YouTube bot detection
            # ── on headless servers like HuggingFace Spaces
            yt_cmd = [
                "yt-dlp",
                "--extractor-args", "youtube:player_client=ios",
                "--no-check-certificates",
                "-f", "bestaudio",
                "--get-url",
                self.source_url
            ]

            try:

                result = subprocess.run(
                    yt_cmd,
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if result.returncode != 0:
                    log_message(
                        f"yt-dlp failed: {result.stderr.strip()}"
                    )
                    raise RuntimeError(
                        f"yt-dlp error: {result.stderr.strip()}"
                    )

                audio_url = result.stdout.strip()

                if not audio_url:
                    raise RuntimeError(
                        "yt-dlp returned empty URL"
                    )

                log_message(
                    "Extracted audio URL successfully"
                )

            except subprocess.TimeoutExpired:

                log_message("yt-dlp timed out after 30s")
                raise

        else:

            audio_url = self.source_url

        process = (
            ffmpeg
            .input(audio_url)
            .output(
                'pipe:',
                format='s16le',
                acodec='pcm_s16le',
                ac=1,
                ar=sr
            )
            .run_async(
                pipe_stdout=True,
                pipe_stderr=True
            )
        )

        def generator():

            while self.running:

                in_bytes = process.stdout.read(4096)

                if not in_bytes:

                    log_message("Audio stream closed")

                    break

                audio_np = (
                    np.frombuffer(in_bytes, np.int16)
                    .astype(np.float32)
                    / 32768.0
                )

                yield audio_np

            # cleanup ffmpeg process
            try:
                process.stdout.close()
                process.wait(timeout=5)
            except Exception:
                process.kill()

        return generator(), sr

    # =====================================================
    # KEYWORDS
    # =====================================================

    def add_keyword(self, kw):

        kw = kw.lower().strip()

        if kw and kw not in self.keywords:
            self.keywords.append(kw)

    def remove_keyword(self, kw):

        kw = kw.lower().strip()

        self.keywords = [
            k for k in self.keywords
            if k != kw
        ]

    # =====================================================
    # DIARIZATION
    # =====================================================

    def _run_diarization(self):

        if DIARIZATION_PIPELINE is None:

            log_message("Diarization pipeline unavailable")

            return

        if len(self.full_audio) < 16000:

            log_message("Not enough audio for diarization")

            return

        try:

            temp_wav = os.path.join(
                TRANSCRIPTS_DIR,
                "temp_audio.wav"
            )

            sf.write(
                temp_wav,
                np.array(self.full_audio),
                16000
            )

            diarization = DIARIZATION_PIPELINE(temp_wav)

            speakers = set()

            for _, _, speaker in diarization.itertracks(
                yield_label=True
            ):
                speakers.add(speaker)

            log_message(
                f"Diarization complete: "
                f"{len(speakers)} speakers detected"
            )

            os.remove(temp_wav)

        except Exception as e:

            log_message(f"Diarization failed: {e}")

    # =====================================================
    # SAVE TRANSCRIPT
    # =====================================================

    def _save_transcript(self):

        try:

            with open(
                self.transcript_file,
                "w",
                encoding="utf-8"
            ) as f:

                f.write("\n".join(self.transcript_lines))

            log_message(
                f"Transcript saved: {self.transcript_file}"
            )

        except Exception as e:

            log_message(f"Save failed: {e}")

    # =====================================================
    # GETTERS
    # =====================================================

    def get_latest_transcript(self):

        return "\n".join(self.transcript_lines[-80:])

    def get_alerts(self):

        return self.alerts[-20:]