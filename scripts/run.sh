#!/bin/bash

# Function to cleanup processes on exit
cleanup() {
    echo -e "\nShutting down services..."
    kill $SERVER_PID 2>/dev/null
    kill $CLIENT_PID 2>/dev/null
    exit 0
}

# Set up trap for cleanup
trap cleanup SIGINT SIGTERM

# Get the project root directory (parent of scripts directory)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Check if virtual environment exists and activate it
if [ -d "${PROJECT_ROOT}/venv" ]; then
    source "${PROJECT_ROOT}/venv/bin/activate" 2>/dev/null || source "${PROJECT_ROOT}/venv/Scripts/activate" 2>/dev/null
fi

# Create necessary directories if they don't exist
mkdir -p "${PROJECT_ROOT}/backend/app/"{api,core,models} \
         "${PROJECT_ROOT}/backend/config" \
         "${PROJECT_ROOT}/frontend/app/utils" \
         "${PROJECT_ROOT}/frontend/config"

# Add project root to PYTHONPATH
export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH}"

# Start FastAPI server
echo "Starting FastAPI server..."
cd "${PROJECT_ROOT}/backend" && python main.py &
SERVER_PID=$!

# Wait for server to start
sleep 2

# Start Streamlit client
echo "Starting Streamlit client..."
cd "${PROJECT_ROOT}/frontend" && streamlit run app/main.py &
CLIENT_PID=$!

# Wait for either process to exit
wait $SERVER_PID $CLIENT_PID

# Cleanup on exit
cleanup