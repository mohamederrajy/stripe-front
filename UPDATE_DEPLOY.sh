#!/bin/bash

# Quick Update Script for Stripe Rebilling Dashboard
# Run this on the server when you push updates to GitHub

echo "🔄 Updating Stripe Rebilling Dashboard..."
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo "✅ Running as root"
else
    echo "⚠️  Please run as root or with sudo"
    exit 1
fi

echo "📥 Pulling latest backend code..."
cd /var/www/stripe-app/backend
git pull

echo ""
echo "🐍 Installing/updating Python dependencies..."
pip3 install -r requirements.txt

echo ""
echo "🔄 Restarting backend..."
supervisorctl restart stripe-backend
sleep 2
supervisorctl status stripe-backend

echo ""
echo "📥 Pulling latest frontend code..."
cd /var/www/stripe-app/frontend
git pull

echo ""
echo "🔧 Ensuring API URL is correct..."
sed -i "s|const API_URL = 'http://localhost:5001';|const API_URL = 'https://api.stripech.dev';|g" /var/www/stripe-app/frontend/index.html

echo ""
echo "🔒 Setting permissions..."
chown -R www-data:www-data /var/www/stripe-app
chmod -R 755 /var/www/stripe-app

echo ""
echo "🔄 Reloading Nginx..."
nginx -t && systemctl reload nginx

echo ""
echo "=========================================="
echo "✅ Update Complete!"
echo "=========================================="
echo ""
echo "🌐 Your updated sites:"
echo "   Frontend: https://stripech.dev"
echo "   Backend:  https://api.stripech.dev"
echo ""
echo "📊 Check status:"
echo "   supervisorctl status stripe-backend"
echo "   tail -f /var/log/stripe-backend.out.log"
echo ""

