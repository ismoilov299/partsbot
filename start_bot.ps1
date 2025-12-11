# PowerShell script to start the bot
# This script activates venv and starts the bot

Write-Host "Starting Zapchast Bot..." -ForegroundColor Green

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Check if Redis is running
Write-Host "Checking Redis connection..." -ForegroundColor Yellow

try {
    # Try to connect to Redis
    $pythonCheck = python -c "import redis; r = redis.Redis(host='localhost', port=6379, db=0); r.ping(); print('OK')" 2>&1
    
    if ($pythonCheck -notlike "*OK*") {
        Write-Host "❌ Cannot connect to Redis!" -ForegroundColor Red
        Write-Host "Please start Redis first:" -ForegroundColor Yellow
        Write-Host "  1. Run: .\start_redis.ps1" -ForegroundColor Cyan
        Write-Host "  2. Or see REDIS_SETUP.md for installation" -ForegroundColor Cyan
        exit 1
    }
    
    Write-Host "✅ Redis is running" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Warning: Could not verify Redis connection" -ForegroundColor Yellow
}

# Start the bot
Write-Host ""
Write-Host "Starting bot..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

python run.py
