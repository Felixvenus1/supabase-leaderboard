# Supabase Real-Time Leaderboard

Project 03 from the portfolio BRD. This app uses Streamlit for the UI and Supabase for cloud PostgreSQL persistence.

## Features

- Submit player name, game name, and score
- Store records in Supabase table: leaderboard
- Render top 20 scores sorted by score descending
- Enforce positive score validation
- Auto-refresh leaderboard for near real-time updates

## Tech Stack

- Streamlit
- supabase-py
- python-dotenv

## Setup

1. Create and activate your virtual environment.
2. Install dependencies:
   pip install -r requirements.txt
3. Copy environment template:
   copy .env.example .env
4. Add your Supabase values to .env:
   SUPABASE_URL=your_project_url
   SUPABASE_KEY=your_anon_key
5. Ensure your Supabase table exists using sql/schema.sql.
6. (Optional local convenience) copy Streamlit secrets template:
   copy .streamlit\secrets.toml.example .streamlit\secrets.toml

## Run

streamlit run app.py

## Streamlit Cloud Deployment

1. Push this repository to GitHub.
2. In Streamlit Community Cloud, create a new app from this repo.
3. Set main file path to: app.py
4. In app settings, add Secrets:
   SUPABASE_URL = your project URL
   SUPABASE_KEY = your anon key
5. Deploy.

## Security Notes

- Never commit .env or .streamlit/secrets.toml.
- If a key is accidentally shared publicly, rotate it in Supabase.
- Enable RLS and strict policies before public launch.

## File Structure

- app.py
- src/db.py
- src/leaderboard.py
- sql/schema.sql
- docs/dataflow.md
- .streamlit/config.toml
- .streamlit/secrets.toml.example
- tests/test_leaderboard.py

## Security Note

Never commit .env to Git. Keep your project keys in environment variables only.
