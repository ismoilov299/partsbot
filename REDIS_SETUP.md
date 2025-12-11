# Redis Setup Instructions for Windows

## Option 1: Using WSL (Windows Subsystem for Linux) - RECOMMENDED

1. Install WSL if not installed:
```powershell
wsl --install
```

2. Open WSL terminal and install Redis:
```bash
sudo apt update
sudo apt install redis-server -y
```

3. Start Redis:
```bash
sudo service redis-server start
```

4. Test Redis:
```bash
redis-cli ping
```
Should return "PONG"

5. Keep WSL terminal open while bot is running

## Option 2: Using Memurai (Redis for Windows)

1. Download Memurai from: https://www.memurai.com/get-memurai
2. Install and start Memurai service
3. It will run on localhost:6379 by default

## Option 3: Using Docker

1. Install Docker Desktop for Windows
2. Run Redis container:
```powershell
docker run -d -p 6379:6379 --name redis redis:alpine
```

3. Check if running:
```powershell
docker ps
```

## Testing Redis Connection

After starting Redis, test with:
```powershell
# For WSL users
wsl redis-cli ping

# For Memurai/Docker users
redis-cli ping
```

## Bot Configuration

The bot is already configured to use:
- Host: localhost
- Port: 6379
- DB: 0

No changes needed in `.env` file.
