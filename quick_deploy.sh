#!/bin/bash
# Quick deploy script for server 45.132.255.109

SERVER_IP="45.132.255.109"
SERVER_USER="root"
PROJECT_PATH="/home/partsbot"

echo "🚀 Deploying to server $SERVER_IP..."

# SSH va deploy
ssh $SERVER_USER@$SERVER_IP << 'ENDSSH'
cd /home

# Clone project if not exists
if [ ! -d "partsbot" ]; then
    echo "📥 Cloning project..."
    git clone https://github.com/ismoilov299/partsbot.git partsbot
fi

cd partsbot

# Pull latest changes
echo "📥 Pulling latest changes..."
git pull origin main

# Run deploy script
chmod +x deploy.sh
./deploy.sh

echo "✅ Deployment completed!"
echo "🌐 Django Admin: http://45.132.255.109/admin/"
echo "📝 Don't forget to:"
echo "   1. Edit .env file: nano .env"
echo "   2. Create superuser: source venv/bin/activate && python manage.py createsuperuser"
echo "   3. Restart services: sudo systemctl restart zapchastbot zapchast-django"

ENDSSH

echo "✅ Done!"
