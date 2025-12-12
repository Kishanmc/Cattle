#!/usr/bin/env bash
# from within backend/ directory
export PYTHONPATH="$(pwd)/app:$PYTHONPATH"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
