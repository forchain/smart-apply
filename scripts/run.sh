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

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
fi

# Start FastAPI server
echo "Starting FastAPI server..."
cd backend && python main.py &
SERVER_PID=$!

# Wait for server to start
sleep 2

# Start Streamlit client
echo "Starting Streamlit client..."
cd ../frontend && streamlit run app/pages/home.py &
CLIENT_PID=$!

# Wait for either process to exit
wait $SERVER_PID $CLIENT_PID

# Cleanup on exit
cleanup 