# 🚀 Deployment Guide - Stripe Rebilling Dashboard

Deploy to server: **5.78.152.132**
- Frontend: **stripech.dev**
- Backend API: **api.stripech.dev**

---

## 📋 Prerequisites

Before starting, make sure:
- ✅ DNS records are set:
  - `stripech.dev` → `5.78.152.132`
  - `api.stripech.dev` → `5.78.152.132`
- ✅ You have SSH access to the server
- ✅ Server is running Ubuntu/Debian Linux

---

## Step 1: Connect to Your Server

```bash
ssh root@5.78.152.132
# Or if you have a specific user:
# ssh your_user@5.78.152.132
```

---

## Step 2: Update Server & Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python, Nginx, and other tools
sudo apt install -y python3 python3-pip nginx git certbot python3-certbot-nginx

# Install Supervisor (to keep backend running)
sudo apt install -y supervisor
```

---

## Step 3: Clone Your Repositories

```bash
# Create application directory
cd /var/www
sudo mkdir -p stripe-app
cd stripe-app

# Clone backend
sudo git clone https://github.com/mohamederrajy/stripe-backend-.git backend

# Clone frontend
sudo git clone https://github.com/mohamederrajy/stripe-front.git frontend
```

---

## Step 4: Setup Backend (api.stripech.dev)

```bash
# Navigate to backend
cd /var/www/stripe-app/backend

# Install Python dependencies
sudo pip3 install -r requirements.txt

# Create environment file (optional for API keys)
sudo nano .env
# (Leave empty for now, API keys come from frontend)

# Test backend manually
python3 server.py
# Press Ctrl+C to stop after testing
```

---

## Step 5: Configure Supervisor for Backend

Create supervisor config to keep backend running:

```bash
sudo nano /etc/supervisor/conf.d/stripe-backend.conf
```

Paste this content:

```ini
[program:stripe-backend]
directory=/var/www/stripe-app/backend
command=/usr/bin/python3 server.py
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/stripe-backend.err.log
stdout_logfile=/var/log/stripe-backend.out.log
environment=PYTHONUNBUFFERED="1"
```

Start the backend:

```bash
# Reload supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start stripe-backend

# Check status
sudo supervisorctl status stripe-backend
```

---

## Step 6: Configure Nginx for Backend (api.stripech.dev)

```bash
sudo nano /etc/nginx/sites-available/api.stripech.dev
```

Paste this content:

```nginx
server {
    listen 80;
    server_name api.stripech.dev;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS headers
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Content-Type, Authorization' always;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/api.stripech.dev /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## Step 7: Configure Nginx for Frontend (stripech.dev)

```bash
sudo nano /etc/nginx/sites-available/stripech.dev
```

Paste this content:

```nginx
server {
    listen 80;
    server_name stripech.dev www.stripech.dev;
    root /var/www/stripe-app/frontend;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/stripech.dev /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## Step 8: Update Frontend API URL

Update the frontend to use your production API:

```bash
sudo nano /var/www/stripe-app/frontend/index.html
```

Find this line (around line 389):
```javascript
const API_URL = 'http://localhost:5001';
```

Change it to:
```javascript
const API_URL = 'https://api.stripech.dev';
```

Save and exit (Ctrl+X, then Y, then Enter)

---

## Step 9: Setup SSL Certificates (HTTPS)

```bash
# Get SSL for backend API
sudo certbot --nginx -d api.stripech.dev

# Get SSL for frontend
sudo certbot --nginx -d stripech.dev -d www.stripech.dev

# Follow the prompts:
# - Enter your email
# - Agree to terms
# - Choose to redirect HTTP to HTTPS (option 2)
```

Certbot will automatically:
- ✅ Get SSL certificates
- ✅ Configure Nginx for HTTPS
- ✅ Set up auto-renewal

---

## Step 10: Set Permissions

```bash
# Set correct ownership
sudo chown -R www-data:www-data /var/www/stripe-app

# Set correct permissions
sudo chmod -R 755 /var/www/stripe-app
```

---

## Step 11: Configure Firewall

```bash
# Allow HTTP, HTTPS, and SSH
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Check status
sudo ufw status
```

---

## Step 12: Test Your Deployment

Open your browser and visit:

1. **Backend API Health Check:**
   - https://api.stripech.dev/health
   - Should return: `{"status":"ok","message":"Backend is running"}`

2. **Frontend Dashboard:**
   - https://stripech.dev
   - Should show your dashboard

---

## 🔄 Updating Your Application

When you push updates to GitHub:

```bash
# SSH into server
ssh root@5.78.152.132

# Update backend
cd /var/www/stripe-app/backend
sudo git pull
sudo supervisorctl restart stripe-backend

# Update frontend
cd /var/www/stripe-app/frontend
sudo git pull
```

---

## 📊 Monitoring & Logs

### Check Backend Status
```bash
sudo supervisorctl status stripe-backend
```

### View Backend Logs
```bash
# Error logs
sudo tail -f /var/log/stripe-backend.err.log

# Output logs
sudo tail -f /var/log/stripe-backend.out.log
```

### View Nginx Logs
```bash
# Access logs
sudo tail -f /var/log/nginx/access.log

# Error logs
sudo tail -f /var/log/nginx/error.log
```

### Restart Services
```bash
# Restart backend
sudo supervisorctl restart stripe-backend

# Restart nginx
sudo systemctl restart nginx
```

---

## 🔐 Security Checklist

- ✅ SSL certificates installed (HTTPS)
- ✅ Firewall configured (UFW)
- ✅ Backend runs as www-data user (not root)
- ✅ Nginx security headers enabled
- ✅ CORS properly configured
- ⚠️ **Important:** Never commit Stripe API keys to Git!

---

## 🆘 Troubleshooting

### Backend not responding?
```bash
sudo supervisorctl status stripe-backend
sudo supervisorctl restart stripe-backend
```

### Frontend not loading?
```bash
sudo nginx -t
sudo systemctl restart nginx
```

### SSL issues?
```bash
sudo certbot renew --dry-run
sudo certbot certificates
```

### Port 5001 blocked?
```bash
sudo netstat -tlnp | grep 5001
sudo lsof -i :5001
```

---

## 🎉 You're Done!

Your application is now live at:
- 🎨 Frontend: **https://stripech.dev**
- 🔙 Backend: **https://api.stripech.dev**

Test the full workflow:
1. Visit https://stripech.dev
2. Enter your Stripe API key
3. Configure charge settings
4. Start charging customers!

---

## 📞 Support

If you encounter issues:
1. Check the logs (see Monitoring section above)
2. Verify DNS propagation: https://dnschecker.org
3. Test API directly: `curl https://api.stripech.dev/health`
4. Check Nginx config: `sudo nginx -t`
5. Check supervisor: `sudo supervisorctl status`

