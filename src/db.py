from __future__ import annotations

import os

from dotenv import load_dotenv
from supabase import Client, create_client


def get_supabase_client() -> Client:
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in environment.")

    return create_client(url, key)
