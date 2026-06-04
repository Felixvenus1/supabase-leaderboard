from __future__ import annotations

from typing import Any

from src.db import get_supabase_client

TABLE_NAME = "leaderboard"
MAX_PLAYER_NAME_LEN = 100
MAX_GAME_NAME_LEN = 100


def validate_score(score: int) -> None:
    if score <= 0:
        raise ValueError("Score must be a positive integer.")


def validate_player_name(player_name: str) -> str:
    clean_name = player_name.strip()
    if not clean_name:
        raise ValueError("Player name is required.")
    if len(clean_name) > MAX_PLAYER_NAME_LEN:
        raise ValueError(f"Player name must be <= {MAX_PLAYER_NAME_LEN} characters.")
    return clean_name


def normalize_game_name(game_name: str) -> str:
    clean_name = game_name.strip() or "Default Game"
    if len(clean_name) > MAX_GAME_NAME_LEN:
        raise ValueError(f"Game name must be <= {MAX_GAME_NAME_LEN} characters.")
    return clean_name


def submit_score(player_name: str, score: int, game_name: str) -> dict[str, Any]:
    validate_score(score)
    valid_player_name = validate_player_name(player_name)
    valid_game_name = normalize_game_name(game_name)

    payload = {
        "player_name": valid_player_name,
        "score": score,
        "game_name": valid_game_name,
    }

    client = get_supabase_client()
    result = client.table(TABLE_NAME).insert(payload).execute()
    return result.data[0] if result.data else payload


def get_top_scores(limit: int = 20) -> list[dict[str, Any]]:
    if limit <= 0:
        raise ValueError("limit must be greater than 0")

    client = get_supabase_client()
    result = (
        client.table(TABLE_NAME)
        .select("id, player_name, score, game_name, created_at")
        .order("score", desc=True)
        .order("created_at", desc=False)
        .limit(limit)
        .execute()
    )
    return result.data or []
