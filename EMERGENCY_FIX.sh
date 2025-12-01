#!/bin/bash

echo "════════════════════════════════════════"
echo "🚨 EMERGENCY FIX - CLEAN DEPLOYMENT"
echo "════════════════════════════════════════"
echo ""

# Step 1: Update Nginx to disable caching
echo "Step 1: Updating Nginx config..."
cat > /etc/nginx/sites-available/stripech.dev << 'NGINXCONF'
server {
    listen 80;
    server_name stripech.dev;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name stripech.dev;
    
    ssl_certificate /etc/letsencrypt/live/stripech.dev/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/stripech.dev/privkey.pem;
    
    root /var/www/stripe-app/frontend;
    index index.html;
    
    # FORCE NO CACHING
    location / {
        add_header Cache-Control "no-store, no-cache, must-revalidate, max-age=0";
        add_header Pragma "no-cache";
        add_header Expires "0";
        try_files $uri $uri/ /index.html;
    }
}
NGINXCONF

echo "✅ Nginx config written"

# Test nginx
nginx -t
if [ $? -eq 0 ]; then
    systemctl reload nginx
    echo "✅ Nginx reloaded"
else
    echo "❌ Nginx config error!"
    exit 1
fi

# Step 2: Force clean git pull
echo ""
echo "Step 2: Cleaning and updating frontend..."
cd /var/www/stripe-app/frontend

# Reset any local changes
git reset --hard HEAD
git clean -fd

# Force pull from origin
git fetch origin
git reset --hard origin/main

echo "✅ Frontend updated to: $(git log --oneline -1)"

# Step 3: Update backend
echo ""
echo "Step 3: Updating backend..."
cd /var/www/stripe-app/backend

# Reset any local changes
git reset --hard HEAD
git clean -fd

# Force pull from origin
git fetch origin
git reset --hard origin/main

echo "✅ Backend updated to: $(git log --oneline -1)"

# Step 4: Restart backend
echo ""
echo "Step 4: Restarting backend..."
supervisorctl restart stripe-backend
sleep 2
supervisorctl status stripe-backend

echo ""
echo "════════════════════════════════════════"
echo "✅ DEPLOYMENT COMPLETE!"
echo "════════════════════════════════════════"
echo ""
echo "NOW DO THIS:"
echo "1. Close ALL browser tabs with stripech.dev"
echo "2. Open INCOGNITO window (Ctrl+Shift+N)"
echo "3. Go to: https://stripech.dev"
echo "4. Press F12 and look for dashboard loads"
echo ""
echo "Dashboard should work with pause/resume/stop!"
echo "════════════════════════════════════════"

