from __future__ import annotations

import pytest

from src import leaderboard


class DummyResponse:
    def __init__(self, data):
        self.data = data


class DummyQuery:
    def __init__(self, response_data):
        self.response_data = response_data

    def insert(self, _payload):
        return self

    def select(self, _fields):
        return self

    def order(self, *_args, **_kwargs):
        return self

    def limit(self, _n):
        return self

    def execute(self):
        return DummyResponse(self.response_data)


class DummyClient:
    def __init__(self, response_data):
        self.response_data = response_data

    def table(self, _name):
        return DummyQuery(self.response_data)


def test_validate_score_rejects_zero() -> None:
    with pytest.raises(ValueError):
        leaderboard.validate_score(0)


def test_validate_player_name_strips_and_accepts() -> None:
    assert leaderboard.validate_player_name("  Felix  ") == "Felix"


def test_validate_player_name_rejects_blank() -> None:
    with pytest.raises(ValueError):
        leaderboard.validate_player_name("   ")


def test_normalize_game_name_defaults_when_blank() -> None:
    assert leaderboard.normalize_game_name(" ") == "Default Game"


def test_get_top_scores_limit_validation() -> None:
    with pytest.raises(ValueError):
        leaderboard.get_top_scores(limit=0)


def test_submit_score_returns_inserted_row(monkeypatch) -> None:
    sample = [{"id": "1", "player_name": "Felix", "score": 100, "game_name": "Hades"}]
    monkeypatch.setattr(leaderboard, "get_supabase_client", lambda: DummyClient(sample))

    result = leaderboard.submit_score(player_name="Felix", score=100, game_name="Hades")
    assert result["player_name"] == "Felix"
    assert result["score"] == 100


def test_get_top_scores_returns_rows(monkeypatch) -> None:
    sample = [{"player_name": "A", "score": 300}, {"player_name": "B", "score": 200}]
    monkeypatch.setattr(leaderboard, "get_supabase_client", lambda: DummyClient(sample))

    rows = leaderboard.get_top_scores(limit=20)
    assert len(rows) == 2
    assert rows[0]["score"] == 300


def _force_local(monkeypatch) -> None:
    def _raise() -> None:
        raise ValueError("no creds")

    monkeypatch.setattr(leaderboard, "get_supabase_client", _raise)


def test_active_backend_local_without_creds(monkeypatch) -> None:
    _force_local(monkeypatch)
    assert leaderboard.active_backend() == "local"


def test_local_fallback_submit_and_read(monkeypatch, tmp_path) -> None:
    # Point the local store at a throwaway DB and force the local backend.
    monkeypatch.setattr(leaderboard.local_store, "DB_PATH", tmp_path / "lb.db")
    _force_local(monkeypatch)

    leaderboard.submit_score(player_name="Felix", score=150, game_name="Hades")
    leaderboard.submit_score(player_name="Sam", score=300, game_name="Hades")

    rows = leaderboard.get_top_scores(limit=20)
    assert [r["player_name"] for r in rows] == ["Sam", "Felix"]
    assert rows[0]["score"] == 300
    assert "created_at" in rows[0]
