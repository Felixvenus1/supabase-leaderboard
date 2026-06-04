-- Project 03 Supabase leaderboard schema

create table if not exists leaderboard (
    id uuid default gen_random_uuid() primary key,
    player_name varchar(100) not null,
    score integer not null check (score > 0),
    game_name varchar(100) not null default 'Default Game',
    created_at timestamptz default now()
);

create index if not exists idx_leaderboard_score
on leaderboard(score desc, created_at asc);

-- Row Level Security
-- Enable before going public. These policies allow anyone to read and submit
-- scores, which is correct for an open leaderboard. Update and delete are
-- intentionally not permitted via the API.
alter table leaderboard enable row level security;

create policy "leaderboard_select" on leaderboard
    for select using (true);

create policy "leaderboard_insert" on leaderboard
    for insert with check (true);
