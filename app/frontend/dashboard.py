import os
import requests
import streamlit as st
from datetime import datetime
import pandas as pd

# =========================================================
# CONFIG
# =========================================================

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://localhost:9000"
)

st.set_page_config(
    page_title="FlowScribe Enterprise",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# SESSION STATE
# =========================================================

if "selected_stream" not in st.session_state:
    st.session_state.selected_stream = None

# =========================================================
# API HELPERS
# =========================================================

def backend_get(endpoint):

    try:

        response = requests.get(
            f"{BACKEND_URL}{endpoint}",
            timeout=30
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
            timeout=60,
            **kwargs
        )

        return response.json()

    except Exception as e:

        return {
            "message": str(e)
        }

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    background-color: #020617;
    color: white;
}

/* MAIN */

.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    max-width: 100%;
}

/* HEADER */

.main-title {
    font-size: 46px;
    font-weight: 800;
    color: #38bdf8;
    letter-spacing: 1px;
}

.sub-title {
    color: #94a3b8;
    margin-top: -8px;
    margin-bottom: 18px;
    font-size: 18px;
}

.status-online {
    color: #22c55e;
    font-weight: 700;
    font-size: 16px;
    margin-top: 15px;
}

/* METRICS */

.metric-card {
    background: linear-gradient(145deg,#0f172a,#111827);
    border: 1px solid #1e293b;
    border-radius: 18px;
    padding: 22px;
    min-height: 140px;
}

.metric-title {
    color: #94a3b8;
    font-size: 14px;
    margin-bottom: 14px;
}

.metric-value {
    font-size: 42px;
    font-weight: 800;
    color: white;
}

/* PANELS */

.panel {
    background-color: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 18px;
    padding: 20px;
}

/* TRANSCRIPT */

.transcript-box {
    height: 720px;
    overflow-y: auto;
    padding-right: 8px;
}

.transcript-line {
    background-color: #111827;
    border-left: 4px solid #38bdf8;
    margin-bottom: 12px;
    padding: 14px;
    border-radius: 10px;
    line-height: 1.7;
    font-size: 15px;
}

/* ALERT */

.alert-box {
    background-color: #3f0d12;
    border-left: 4px solid #ef4444;
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 10px;
    font-size: 14px;
}

/* STREAM */

.stream-card {
    background-color: #111827;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 10px;
}

/* KEYWORD */

.keyword-chip {
    display: inline-block;
    background-color: #1d4ed8;
    color: white;
    border-radius: 999px;
    padding: 6px 14px;
    margin: 4px;
    font-size: 13px;
}

/* LOG */

.log-entry {
    background-color: #111827;
    border-left: 4px solid #38bdf8;
    padding: 10px;
    border-radius: 8px;
    margin-bottom: 8px;
    font-size: 14px;
}

/* HIDE SIDEBAR */

[data-testid="collapsedControl"] {
    display: none;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# BACKEND DATA
# =========================================================

health = backend_get("/health")

backend_online = (
    health.get("status") == "online"
)

stream_count = health.get(
    "active_streams",
    0
)

keyword_count = health.get(
    "keywords",
    0
)

transcript_data = backend_get("/transcript")

raw_transcript = transcript_data.get(
    "transcript",
    ""
)

if isinstance(raw_transcript, str):

    transcript_lines = [
        line.strip()
        for line in raw_transcript.split("\n")
        if line.strip()
    ]

else:

    transcript_lines = raw_transcript

alerts = transcript_data.get(
    "alerts",
    []
)

# =========================================================
# HEADER
# =========================================================

header1, header2 = st.columns([5,1])

with header1:

    st.markdown("""
    <div class="main-title">
    🎙️ FlowScribe
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sub-title">
    Enterprise Legislative & Courtroom Intelligence Monitoring System
    </div>
    """, unsafe_allow_html=True)

with header2:

    if backend_online:

        st.markdown("""
        <div class="status-online">
        🟢 Backend Connected
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# METRICS
# =========================================================

m1, m2, m3, m4 = st.columns(4)

with m1:

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">
        ACTIVE STREAMS
        </div>

        <div class="metric-value">
        {stream_count}
        </div>
    </div>
    """, unsafe_allow_html=True)

with m2:

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">
        KEYWORD CORPUS
        </div>

        <div class="metric-value">
        {keyword_count}
        </div>
    </div>
    """, unsafe_allow_html=True)

with m3:

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">
        TRANSCRIPT EVENTS
        </div>

        <div class="metric-value">
        {len(transcript_lines)}
        </div>
    </div>
    """, unsafe_allow_html=True)

with m4:

    current_time = datetime.now().strftime("%H:%M:%S")

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">
        SYSTEM TIME
        </div>

        <div class="metric-value">
        {current_time}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# MAIN LAYOUT
# =========================================================

left, center, right = st.columns([1.2, 2.8, 1.2])

# =========================================================
# LEFT PANEL
# =========================================================

with left:

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.subheader("📡 Stream Control")

    stream_url = st.text_input(
        "Stream URL",
        placeholder="YouTube Live / RTSP"
    )

    source_type = st.radio(
        "Source",
        ["youtube", "rtsp"],
        horizontal=True
    )

    if st.button(
        "▶ Start Stream",
        use_container_width=True
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

            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "■ Stop All Streams",
        use_container_width=True
    ):

        backend_post("/stop_all")

        st.warning(
            "All streams stopped"
        )

        st.rerun()

    st.markdown("---")

    st.subheader("🎯 Active Streams")

    stream_data = backend_get("/streams")

    streams = stream_data.get(
        "streams",
        []
    )

    if streams:

        for idx, stream in enumerate(streams):

            st.markdown(
                f"""
                <div class="stream-card">
                <b>Stream {idx+1}</b><br>
                {stream["url"][:70]}
                </div>
                """,
                unsafe_allow_html=True
            )

            colA, colB = st.columns([4,1])

            with colA:

                if st.button(
                    "Select",
                    key=f"select_{idx}",
                    use_container_width=True
                ):

                    st.session_state.selected_stream = (
                        stream["url"]
                    )

            with colB:

                if st.button(
                    "✕",
                    key=f"delete_{idx}"
                ):

                    backend_post(
                        "/stop_stream",
                        params={
                            "url": stream["url"]
                        }
                    )

                    st.rerun()

    else:

        st.info("No active streams")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# CENTER PANEL
# =========================================================

with center:

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.subheader("📝 Live Intelligence Feed")

    transcript_html = ""

    for line in transcript_lines[-100:]:

        transcript_html += f"""
        <div class="transcript-line">
        {line}
        </div>
        """

    st.markdown(f"""
    <div class="transcript-box">
    {transcript_html}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# RIGHT PANEL
# =========================================================

with right:

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.subheader("🚨 Keyword Alerts")

    if alerts:

        for alert in alerts[-20:]:

            st.markdown(f"""
            <div class="alert-box">
            {alert}
            </div>
            """, unsafe_allow_html=True)

    else:

        st.info("No alerts")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.subheader("🔑 Keywords")

    new_keyword = st.text_input(
        "Add Keyword"
    )

    if st.button(
        "Add Keyword",
        use_container_width=True
    ):

        if new_keyword.strip():

            backend_post(
                "/add_keyword",
                json={
                    "keyword": new_keyword
                }
            )

            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    keyword_data = backend_get(
        "/keywords"
    )

    keywords = keyword_data.get(
        "keywords",
        []
    )

    for idx, kw in enumerate(keywords):

        c1, c2 = st.columns([4,1])

        with c1:

            st.markdown(
                f"""
                <span class="keyword-chip">
                {kw}
                </span>
                """,
                unsafe_allow_html=True
            )

        with c2:

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

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# BOTTOM SECTION
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

bottom1, bottom2 = st.columns(2)

# =========================================================
# LOGS
# =========================================================

with bottom1:

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.subheader("🧾 System Logs")

    logs_data = backend_get("/logs")

    logs = logs_data.get(
        "logs",
        []
    )

    if logs:

        for log in logs[-20:]:

            st.markdown(f"""
            <div class="log-entry">
            {log}
            </div>
            """, unsafe_allow_html=True)

    else:

        st.info("No logs available")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# ANALYTICS
# =========================================================

with bottom2:

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.subheader("📊 Analytics")

    stats_df = pd.DataFrame({

        "Metric": [
            "Transcript Events",
            "Alerts",
            "Keywords",
            "Streams"
        ],

        "Value": [
            len(transcript_lines),
            len(alerts),
            len(keywords),
            len(streams)
        ]
    })

    st.dataframe(
        stats_df,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# ARCHIVE
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown('<div class="panel">', unsafe_allow_html=True)

st.subheader("📁 Transcript Archive")

files_data = backend_get(
    "/transcript_files"
)

files = files_data.get(
    "files",
    []
)

if files:

    for file in files:

        c1, c2 = st.columns([8,1])

        with c1:

            st.write(file)

        with c2:

            download_url = (
                f"{BACKEND_URL}"
                f"/download_transcript"
                f"?filename={file}"
            )

            st.link_button(
                "⬇",
                download_url
            )

else:

    st.info(
        "No transcript files found"
    )

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# REFRESH
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

if st.button(
    "🔄 Refresh Dashboard",
    use_container_width=True
):
    st.rerun()