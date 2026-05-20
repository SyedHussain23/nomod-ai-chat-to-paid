#!/usr/bin/env bash
# Local dev — runs backend and frontend in two background processes.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT/backend"
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install -q -r requirements.txt
[ -f .env ] || cp .env.example .env
uvicorn app.main:app --reload --port 8000 &
BACK_PID=$!

cd "$ROOT/frontend"
[ -d node_modules ] || npm install
npm run dev &
FRONT_PID=$!

trap 'kill $BACK_PID $FRONT_PID 2>/dev/null || true' EXIT INT TERM
echo "Backend: http://localhost:8000/docs"
echo "Frontend: http://localhost:5173"
wait
