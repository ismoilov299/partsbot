#!/bin/bash
# Ubuntu server deployment script

echo "🚀 Starting deployment..."

# Update system
echo "📦 Updating system..."
sudo apt update && sudo apt upgrade -y

# Install dependencies
echo "📦 Installing dependencies..."
sudo apt install python3.11 python3.11-venv python3-pip git redis-server nginx -y

# Enable Redis
echo "🔧 Configuring Redis..."
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Create virtual environment
echo "🐍 Creating virtual environment..."
python3.11 -m venv venv

# Activate and install requirements
echo "📦 Installing Python packages..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# Setup .env file
if [ ! -f .env ]; then
    echo "⚙️ Creating .env file..."
    cat > .env << 'EOF'
BOT_TOKEN=your_bot_token_here
ADMIN_CHAT_ID=your_admin_chat_id
DATABASE_URL=sqlite:///./db.sqlite3
REDIS_HOST=localhost
REDIS_PORT=6379
DJANGO_SECRET_KEY=your_secret_key_here
DEBUG=False
ALLOWED_HOSTS=*
EOF
    echo "⚠️ Please edit .env file with your credentials!"
fi

# Setup database
echo "🗄️ Setting up database..."
python manage.py migrate
python init_db.py

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create systemd service for bot
echo "🤖 Creating bot service..."
sudo tee /etc/systemd/system/zapchastbot.service > /dev/null << EOF
[Unit]
Description=Zapchast Bot
After=network.target redis.service

[Service]
Type=simple
User=$USER
WorkingDirectory=/home/partsbot
Environment="PATH=/home/partsbot/venv/bin"
ExecStart=/home/partsbot/venv/bin/python /home/partsbot/run.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create systemd service for Django
echo "🌐 Creating Django service..."
sudo tee /etc/systemd/system/zapchast-django.service > /dev/null << EOF
[Unit]
Description=Zapchast Django Admin
After=network.target

[Service]
Type=notify
User=$USER
WorkingDirectory=/home/partsbot
Environment="PATH=/home/partsbot/venv/bin"
ExecStart=/home/partsbot/venv/bin/gunicorn src.django_app.wsgi:application --bind 127.0.0.1:8000 --workers 3
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
echo "🔧 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/zapchast-admin > /dev/null << 'EOF'
server {
    listen 80;
    server_name _;

    location /static/ {
        alias /home/partsbot/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/zapchast-admin /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test and restart Nginx
sudo nginx -t && sudo systemctl restart nginx

# Enable and start services
echo "🚀 Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable zapchastbot zapchast-django
sudo systemctl start zapchastbot zapchast-django

# Configure firewall
echo "🔒 Configuring firewall..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
echo "y" | sudo ufw enable

echo "✅ Deployment completed!"
echo ""
echo "📊 Service status:"
sudo systemctl status zapchastbot --no-pager
sudo systemctl status zapchast-django --no-pager
echo ""
echo "🌐 Access Django admin at: http://YOUR_SERVER_IP/admin/"
echo ""
echo "📝 Next steps:"
echo "1. Edit .env file: nano .env"
echo "2. Create superuser: python manage.py createsuperuser"
echo "3. Restart services: sudo systemctl restart zapchastbot zapchast-django"
echo "4. View logs: sudo journalctl -u zapchastbot -f"
