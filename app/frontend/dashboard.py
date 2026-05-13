# app/frontend/dashboard.py

import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

BACKEND_URL = "http://localhost:9000"

st.set_page_config(
    page_title="FlowScribe Enterprise",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st_autorefresh(interval=3000, key="flowscribe_refresh")

# =========================================================
# STYLING
# =========================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    background-color: #040814;
    color: white;
    font-family: Inter;
}

.block-container {
    padding-top: 1rem;
    max-width: 100%;
}

.metric-card {
    background: linear-gradient(145deg,#081225,#0a1630);
    border: 1px solid rgba(80,120,255,0.15);
    border-radius: 22px;
    padding: 24px;
    height: 170px;
}

.metric-title {
    color: #9fb4d3;
    font-size: 15px;
    margin-bottom: 20px;
}

.metric-value {
    font-size: 54px;
    font-weight: 700;
    color: white;
}

.main-panel {
    background: #071225;
    border-radius: 24px;
    padding: 24px;
    border: 1px solid rgba(80,120,255,0.12);
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 18px;
}

.feed-box {
    background: #020817;
    border-radius: 18px;
    height: 640px;
    overflow-y: auto;
    padding: 20px;
    border: 1px solid rgba(80,120,255,0.1);
}

.feed-line {
    background: rgba(80,120,255,0.08);
    padding: 14px;
    border-radius: 12px;
    margin-bottom: 12px;
    font-size: 15px;
    line-height: 1.7;
}

.alert-box {
    background: rgba(255,80,80,0.08);
    border-left: 4px solid #ff5c5c;
    padding: 14px;
    border-radius: 12px;
    margin-bottom: 12px;
}

.stream-card {
    background: #081225;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 16px;
    border: 1px solid rgba(80,120,255,0.12);
}

.keyword-pill {
    display: inline-block;
    background: #2457ff;
    color: white;
    padding: 8px 16px;
    border-radius: 999px;
    margin: 5px;
    font-size: 14px;
}

hr {
    border-color: rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# API HELPERS
# =========================================================

def safe_get(endpoint):

    try:

        response = requests.get(
            f"{BACKEND_URL}{endpoint}",
            timeout=10
        )

        return response.json()

    except Exception as e:

        return {
            "error": str(e)
        }

def safe_post(endpoint, payload=None):

    try:

        response = requests.post(
            f"{BACKEND_URL}{endpoint}",
            params=payload,
            timeout=10
        )

        return response.json()

    except Exception as e:

        return {
            "error": str(e)
        }

# =========================================================
# FETCH DATA
# =========================================================

health = safe_get("/health")
streams = safe_get("/streams").get("streams", [])
keywords = safe_get("/keywords").get("keywords", [])
logs = safe_get("/logs").get("logs", [])
transcript_data = safe_get("/transcript")

transcript_lines = transcript_data.get("transcript", [])
alerts = transcript_data.get("alerts", [])

backend_connected = health.get("status") == "online"

# =========================================================
# HEADER
# =========================================================

c1, c2 = st.columns([8,2])

with c1:

    st.markdown("""
    <div style="display:flex;align-items:center;gap:18px;">
        <div style="font-size:60px;">🎙️</div>
        <div>
            <div style="font-size:58px;font-weight:800;color:#38bdf8;">
                FlowScribe
            </div>
            <div style="font-size:18px;color:#9fb4d3;">
                Enterprise Legislative & Courtroom Intelligence Monitoring System
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:

    if backend_connected:
        st.success("Backend Connected")
    else:
        st.error("Backend Offline")

# =========================================================
# METRICS
# =========================================================

stream_count = len(streams)
keyword_count = len(keywords)
event_count = len(transcript_lines)

m1, m2, m3, m4 = st.columns(4)

with m1:

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">ACTIVE STREAMS</div>
        <div class="metric-value">{stream_count}</div>
    </div>
    """, unsafe_allow_html=True)

with m2:

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">KEYWORD CORPUS</div>
        <div class="metric-value">{keyword_count}</div>
    </div>
    """, unsafe_allow_html=True)

with m3:

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">TRANSCRIPT EVENTS</div>
        <div class="metric-value">{event_count}</div>
    </div>
    """, unsafe_allow_html=True)

with m4:

    current_time = datetime.now().strftime("%H:%M:%S")

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">SYSTEM TIME</div>
        <div class="metric-value">{current_time}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# LAYOUT
# =========================================================

left, center, right = st.columns([1.1, 2.3, 1])

# =========================================================
# LEFT PANEL
# =========================================================

with left:

    st.markdown('<div class="main-panel">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">📡 Stream Control</div>',
        unsafe_allow_html=True
    )

    stream_url = st.text_input("Stream URL")

    source_type = st.radio(
        "Source",
        ["youtube", "rtsp"],
        horizontal=True
    )

    if st.button(
        "▶ Start Stream",
        use_container_width=True
    ):

        result = safe_post(
            "/start_stream",
            {
                "url": stream_url,
                "source_type": source_type
            }
        )

        if "error" in result:
            st.error(result["error"])
        else:
            st.success("Stream started")

    if st.button(
        "⏹ Stop All Streams",
        use_container_width=True
    ):

        safe_post("/stop_all")

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">🎯 Active Streams</div>',
        unsafe_allow_html=True
    )

    for idx, stream in enumerate(streams):

        c1, c2 = st.columns([5,1])

        with c1:

            st.markdown(f"""
            <div class="stream-card">
                <b>Stream {idx+1}</b><br><br>
                {stream.get("url","")}
            </div>
            """, unsafe_allow_html=True)

        with c2:

            if st.button(
                "✔",
                key=f"select_{idx}",
                use_container_width=True
            ):

                st.session_state["selected_stream"] = idx

            if st.button(
                "✕",
                key=f"delete_{idx}",
                use_container_width=True
            ):

                safe_post(
                    "/stop_stream",
                    {
                        "url": stream.get("url", "")
                    }
                )

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# CENTER PANEL
# =========================================================

with center:

    st.markdown('<div class="main-panel">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">📝 Live Intelligence Feed</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="feed-box">', unsafe_allow_html=True)

    if len(transcript_lines) == 0:

        st.warning("No live transcript data received from backend")

    else:

        for line in transcript_lines[-120:]:

            st.markdown(
                f"""
                <div class="feed-line">
                {line}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">📜 System Logs</div>',
        unsafe_allow_html=True
    )

    if len(logs) == 0:

        st.info("No logs available")

    else:

        for log in logs[-15:]:

            st.markdown(
                f"""
                <div class="feed-line">
                {log}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# RIGHT PANEL
# =========================================================

with right:

    st.markdown('<div class="main-panel">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">🚨 Keyword Alerts</div>',
        unsafe_allow_html=True
    )

    if len(alerts) == 0:

        st.info("No alerts")

    else:

        for alert in alerts[-20:]:

            st.markdown(
                f"""
                <div class="alert-box">
                {alert}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">🔑 Keywords</div>',
        unsafe_allow_html=True
    )

    new_keyword = st.text_input("Add Keyword")

    if st.button(
        "Add Keyword",
        use_container_width=True
    ):

        safe_post(
            "/add_keyword",
            {
                "keyword": new_keyword
            }
        )

    for idx, keyword in enumerate(keywords):

        k1, k2 = st.columns([5,1])

        with k1:

            st.markdown(
                f'<div class="keyword-pill">{keyword}</div>',
                unsafe_allow_html=True
            )

        with k2:

            if st.button(
                "✕",
                key=f"kw_delete_{idx}",
                use_container_width=True
            ):

                safe_post(
                    "/remove_keyword",
                    {
                        "keyword": keyword
                    }
                )

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">📊 Analytics</div>',
        unsafe_allow_html=True
    )

    analytics_df = pd.DataFrame(
        {
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
        }
    )

    st.dataframe(
        analytics_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown('</div>', unsafe_allow_html=True)