import os
import requests
import pandas as pd
import streamlit as st
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://localhost:9000"
)

st.set_page_config(
    page_title="FlowScribe",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# SESSION STATE
# =========================================================

if "refresh_counter" not in st.session_state:
    st.session_state.refresh_counter = 0

# =========================================================
# HELPERS
# =========================================================

def backend_get(endpoint):

    try:

        response = requests.get(
            f"{BACKEND_URL}{endpoint}",
            timeout=15
        )

        return response.json()

    except Exception as e:

        return {
            "error": str(e)
        }

def backend_post(endpoint, **kwargs):

    try:

        response = requests.post(
            f"{BACKEND_URL}{endpoint}",
            timeout=30,
            **kwargs
        )

        return response.json()

    except Exception as e:

        return {
            "message": str(e)
        }

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    background-color: #0b1120;
    color: white;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

.main-title {
    font-size: 40px;
    font-weight: 700;
    color: #38bdf8;
}

.sub-title {
    color: #94a3b8;
    margin-bottom: 20px;
}

.metric-card {
    background-color: #111827;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #1e293b;
}

.transcript-panel {
    background-color: #0f172a;
    border-radius: 14px;
    padding: 20px;
    border: 1px solid #1e293b;
    height: 650px;
    overflow-y: auto;
}

.alert-card {
    background-color: #450a0a;
    border: 1px solid #dc2626;
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 10px;
}

.keyword-chip {
    display: inline-block;
    background-color: #1d4ed8;
    color: white;
    padding: 6px 12px;
    margin: 4px;
    border-radius: 999px;
    font-size: 13px;
}

.status-online {
    color: #22c55e;
    font-weight: bold;
}

.stream-card {
    background-color: #111827;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 12px;
}

.log-box {
    background-color: #111827;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 8px;
    border-left: 4px solid #38bdf8;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

health = backend_get("/health")

backend_online = (
    health.get("status") == "online"
)

active_streams_count = health.get(
    "active_streams",
    0
)

keyword_count = health.get(
    "keywords",
    0
)

header_col1, header_col2 = st.columns([4,1])

with header_col1:

    st.markdown(
        """
        <div class="main-title">
        🎙️ FlowScribe
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sub-title">
        Real-time Legislative & Courtroom
        Transcription Monitoring Platform
        </div>
        """,
        unsafe_allow_html=True
    )

with header_col2:

    if backend_online:

        st.markdown(
            """
            <p class="status-online">
            🟢 Backend Connected
            </p>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# TOP METRICS
# =========================================================

m1, m2, m3 = st.columns(3)

with m1:

    st.markdown(
        f"""
        <div class="metric-card">
        <h3>📡 Active Streams</h3>
        <h1>{active_streams_count}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with m2:

    st.markdown(
        f"""
        <div class="metric-card">
        <h3>🔑 Keywords</h3>
        <h1>{keyword_count}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with m3:

    current_time = datetime.now().strftime(
        "%H:%M:%S"
    )

    st.markdown(
        f"""
        <div class="metric-card">
        <h3>🕒 System Time</h3>
        <h1>{current_time}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# TABS
# =========================================================

tabs = st.tabs([
    "📊 Dashboard",
    "📡 Active Streams",
    "🔑 Keyword Management",
    "📁 Transcript Archive",
    "🧾 System Logs",
    "📈 Analytics"
])

# =========================================================
# DASHBOARD TAB
# =========================================================

with tabs[0]:

    col1, col2 = st.columns([3,1])

    # =========================================
    # LIVE TRANSCRIPT
    # =========================================

    with col1:

        st.subheader("📝 Live Transcript")

        transcript_data = backend_get(
            "/transcript"
        )

        transcript_lines = transcript_data.get(
            "transcript",
            []
        )

        transcript_html = ""

        for line in transcript_lines:

            transcript_html += (
                f"<p style='margin-bottom:10px;'>"
                f"{line}"
                f"</p>"
            )

        st.markdown(
            f"""
            <div class="transcript-panel">
            {transcript_html}
            </div>
            """,
            unsafe_allow_html=True
        )

    # =========================================
    # ALERTS
    # =========================================

    with col2:

        st.subheader("🚨 Alerts")

        alerts = transcript_data.get(
            "alerts",
            []
        )

        if alerts:

            for alert in reversed(alerts):

                st.markdown(
                    f"""
                    <div class="alert-card">
                    {alert}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.info(
                "No alerts detected"
            )

# =========================================================
# ACTIVE STREAMS TAB
# =========================================================

with tabs[1]:

    st.subheader("📡 Stream Management")

    stream_url = st.text_input(
        "Stream URL",
        placeholder=(
            "Paste YouTube Live or RTSP URL"
        )
    )

    source_type = st.radio(
        "Source Type",
        ["youtube", "rtsp"],
        horizontal=True
    )

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "▶ Start Stream"
        ):

            if stream_url.strip():

                result = backend_post(
                    "/start_stream",
                    params={
                        "url": stream_url.strip(),
                        "source_type": source_type
                    }
                )

                st.success(
                    result.get(
                        "message",
                        "Started"
                    )
                )

    with c2:

        if st.button(
            "■ Stop All Streams"
        ):

            result = backend_post(
                "/stop_all"
            )

            st.warning(
                result.get(
                    "message",
                    "Stopped"
                )
            )

    st.markdown("---")

    stream_data = backend_get(
        "/streams"
    )

    streams = stream_data.get(
        "streams",
        []
    )

    if streams:

        for idx, stream in enumerate(streams):

            s1, s2 = st.columns([8,1])

            with s1:

                st.markdown(
                    f"""
                    <div class="stream-card">
                    <b>URL:</b> {stream['url']}<br>
                    <b>Type:</b> {stream['type']}<br>
                    <b>Status:</b> 🟢 Running
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with s2:

                if st.button(
                    "✕",
                    key=f"remove_{idx}"
                ):

                    backend_post(
                        "/stop_stream",
                        params={
                            "url": stream["url"]
                        }
                    )

                    st.rerun()

    else:

        st.info(
            "No active streams"
        )

# =========================================================
# KEYWORD TAB
# =========================================================

with tabs[2]:

    st.subheader(
        "🔑 Keyword Corpus Management"
    )

    keyword_data = backend_get(
        "/keywords"
    )

    keywords = keyword_data.get(
        "keywords",
        []
    )

    add_col1, add_col2 = st.columns([4,1])

    with add_col1:

        new_keyword = st.text_input(
            "Add Keyword"
        )

    with add_col2:

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Add"):

            if new_keyword.strip():

                backend_post(
                    "/add_keyword",
                    json={
                        "keyword": new_keyword
                    }
                )

                st.rerun()

    st.markdown("---")

    st.markdown(
        "### Current Keyword Corpus"
    )

    for idx, kw in enumerate(keywords):

        k1, k2 = st.columns([8,1])

        with k1:

            st.markdown(
                f"""
                <span class="keyword-chip">
                {kw}
                </span>
                """,
                unsafe_allow_html=True
            )

        with k2:

            if st.button(
                "✕",
                key=f"kw_{idx}"
            ):

                backend_post(
                    "/remove_keyword",
                    json={
                        "keyword": kw
                    }
                )

                st.rerun()

# =========================================================
# TRANSCRIPT ARCHIVE
# =========================================================

with tabs[3]:

    st.subheader(
        "📁 Transcript Archive"
    )

    files_data = backend_get(
        "/transcript_files"
    )

    files = files_data.get(
        "files",
        []
    )

    if files:

        for file in files:

            d1, d2 = st.columns([6,1])

            with d1:
                st.write(file)

            with d2:

                download_url = (
                    f"{BACKEND_URL}"
                    f"/download_transcript"
                    f"?filename={file}"
                )

                st.link_button(
                    "Download",
                    download_url
                )

    else:

        st.info(
            "No transcript files found"
        )

# =========================================================
# SYSTEM LOGS
# =========================================================

with tabs[4]:

    st.subheader(
        "🧾 System Logs"
    )

    logs_data = backend_get(
        "/logs"
    )

    logs = logs_data.get(
        "logs",
        []
    )

    if logs:

        for log in reversed(logs):

            st.markdown(
                f"""
                <div class="log-box">
                {log}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.info(
            "No logs available"
        )

# =========================================================
# ANALYTICS
# =========================================================

with tabs[5]:

    st.subheader(
        "📈 Analytics"
    )

    st.info(
        "Analytics module will display:\n"
        "- Keyword frequency\n"
        "- Speaker counts\n"
        "- Stream duration\n"
        "- Alert timeline\n"
        "- Session metrics"
    )

# =========================================================
# FOOTER
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🔄 Refresh Dashboard"):

    st.rerun()