"""Local SQLite fallback backend for the leaderboard.

Used automatically when no Supabase credentials are configured, so the app (and
its tests/screenshots) run fully offline in a self-contained "demo mode" that
mirrors the Supabase table contract.
"""

from __future__ import annotations

import os
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DB_PATH = Path(os.getenv("LEADERBOARD_DB", Path(__file__).parent.parent / "leaderboard_local.db"))

_SCHEMA = """
CREATE TABLE IF NOT EXISTS leaderboard (
    id TEXT PRIMARY KEY,
    player_name TEXT NOT NULL,
    score INTEGER NOT NULL CHECK (score > 0),
    game_name TEXT NOT NULL DEFAULT 'Default Game',
    created_at TEXT NOT NULL
);
"""


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute(_SCHEMA)
    return conn


def insert_score(payload: dict[str, Any]) -> dict[str, Any]:
    """Insert a score row and return it (mirrors Supabase insert().execute())."""
    row = {
        "id": str(uuid.uuid4()),
        "player_name": payload["player_name"],
        "score": int(payload["score"]),
        "game_name": payload.get("game_name", "Default Game"),
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    with _connect() as conn:
        conn.execute(
            "INSERT INTO leaderboard (id, player_name, score, game_name, created_at) "
            "VALUES (:id, :player_name, :score, :game_name, :created_at)",
            row,
        )
    return row


def top_scores(limit: int = 20) -> list[dict[str, Any]]:
    """Return the top *limit* rows ordered by score desc, created_at asc."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, player_name, score, game_name, created_at FROM leaderboard "
            "ORDER BY score DESC, created_at ASC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]
