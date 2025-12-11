# PowerShell script to start Redis (WSL)
# Run this before starting the bot

Write-Host "Starting Redis server in WSL..." -ForegroundColor Green

# Check if WSL is installed
$wslInstalled = Get-Command wsl -ErrorAction SilentlyContinue

if (-not $wslInstalled) {
    Write-Host "WSL is not installed. Please install WSL first." -ForegroundColor Red
    Write-Host "Run: wsl --install" -ForegroundColor Yellow
    exit 1
}

# Start Redis in WSL
Write-Host "Starting Redis..." -ForegroundColor Yellow
wsl sudo service redis-server start

# Test connection
Write-Host "Testing Redis connection..." -ForegroundColor Yellow
$redisTest = wsl redis-cli ping

if ($redisTest -eq "PONG") {
    Write-Host "✅ Redis is running successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Redis failed to start. Please check installation." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Redis is ready. You can now start the bot with: python run.py" -ForegroundColor Cyan
