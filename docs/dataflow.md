sequenceDiagram
    participant U as User
    participant S as Streamlit App
    participant C as Supabase Python Client
    participant A as Supabase Data API
    participant P as PostgreSQL

    U->>S: Submit player name + score
    S->>S: Validate score > 0
    S->>C: Insert leaderboard row
    C->>A: REST insert request
    A->>P: Persist row
    P-->>A: Row inserted
    A-->>S: Insert confirmed

    Note over S: st_autorefresh polls at configurable interval (default 8s)

    S->>C: Fetch top 20 rows
    C->>A: REST select request
    A->>P: Query leaderboard ORDER BY score DESC
    P-->>A: Ranked rows
    A-->>C: JSON response
    C-->>S: Leaderboard data
    S-->>U: Render updated table
