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

# Function to check and install dependencies
check_dependencies() {
    local dir=$1
    if [ -f "${dir}/requirements.txt" ]; then
        echo "Checking dependencies in ${dir}..."
        pip install -r "${dir}/requirements.txt" >/dev/null 2>&1
    fi
}

# Install dependencies
check_dependencies "${PROJECT_ROOT}/backend"
check_dependencies "${PROJECT_ROOT}/frontend"

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