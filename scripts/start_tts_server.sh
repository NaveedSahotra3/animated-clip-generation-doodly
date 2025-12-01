#!/bin/bash
# Start the TTS API Server

cd "$(dirname "$0")/.."

echo "🚀 Starting TTS API Server..."
echo ""

python3 scripts/tts_api_server.py "$@"

