from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from src.leaderboard import get_top_scores, submit_score

st.set_page_config(page_title="Supabase Leaderboard", page_icon="Trophy", layout="wide")
st.title("Supabase Real-Time Leaderboard")
st.caption("Project 03 - Streamlit + Supabase")

with st.sidebar:
    st.header("Display Settings")
    auto_refresh = st.toggle("Auto-refresh leaderboard", value=True)
    refresh_seconds = st.slider("Refresh interval (seconds)", min_value=3, max_value=30, value=8)

if auto_refresh:
    st_autorefresh(interval=refresh_seconds * 1000, key="leaderboard_refresh")

with st.form("submit_score_form", clear_on_submit=True):
    player_name = st.text_input("Player Name", max_chars=100)
    game_name = st.text_input("Game Name", value="Default Game", max_chars=100)
    score = st.number_input("Score", min_value=1, step=1)
    submitted = st.form_submit_button("Submit Score")

if submitted:
    try:
        submit_score(player_name=player_name, score=int(score), game_name=game_name)
        st.success("Score submitted successfully.")
    except Exception as exc:
        st.error(f"Submission failed: {exc}")

st.subheader("Top 20 Leaderboard")
try:
    rows = get_top_scores(limit=20)
    if rows:
        df = pd.DataFrame(rows)
        df.index = range(1, len(df) + 1)
        df.index.name = "Rank"
        st.dataframe(df[["player_name", "score", "game_name", "created_at"]], use_container_width=True)
        loaded_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        st.caption(f"Last refreshed: {loaded_at}")
    else:
        st.info("No leaderboard data yet. Submit the first score.")
except Exception as exc:
    st.error(f"Could not load leaderboard: {exc}")
