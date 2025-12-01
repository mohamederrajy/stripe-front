#!/bin/bash
#
# Quick Start Script for Stripe Rebilling Dashboard
# Starts both backend and frontend servers
#

echo "============================================================"
echo "🚀 Starting Stripe Rebilling Dashboard"
echo "============================================================"
echo ""

# Check if in correct directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Must run from stripe-rebill directory"
    echo "   cd /Users/aziz/Downloads/stripe-rebill"
    echo "   ./start_dashboard.sh"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.7+"
    exit 1
fi

# Check Node
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 14+"
    exit 1
fi

# Install backend dependencies if needed
if [ ! -d "backend/__pycache__" ]; then
    echo "📦 Installing backend dependencies..."
    cd backend
    pip3 install -r requirements.txt -q
    cd ..
fi

# Install frontend dependencies if needed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies (this may take a minute)..."
    cd frontend
    npm install --silent
    cd ..
fi

echo ""
echo "✅ All dependencies installed!"
echo ""
echo "🚀 Starting servers..."
echo ""
echo "Backend will run on: http://localhost:5000"
echo "Frontend will run on: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""
echo "============================================================"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Stopping servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup INT TERM

# Start backend
cd backend
python3 app.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 2

# Start frontend
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

# Wait for both processes
wait

