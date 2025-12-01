# 🚀 Deploy NOW - Quick Start

## Option 1: Automated Deployment (Recommended)

### On Your Local Machine:
```bash
# Upload deployment script to server
scp QUICK_DEPLOY.sh root@5.78.152.132:/root/
scp UPDATE_DEPLOY.sh root@5.78.152.132:/root/
```

### On Your Server (SSH):
```bash
# Connect to server
ssh root@5.78.152.132

# Make script executable
chmod +x /root/QUICK_DEPLOY.sh

# Run deployment
./QUICK_DEPLOY.sh
```

### After Script Completes - Setup SSL:
```bash
# Get SSL for backend
certbot --nginx -d api.stripech.dev

# Get SSL for frontend
certbot --nginx -d stripech.dev -d www.stripech.dev
```

**Done! Visit: https://stripech.dev**

---

## Option 2: Manual Step-by-Step

Follow the complete guide in **DEPLOYMENT_GUIDE.md**

### Quick Command Summary:

```bash
# 1. Connect to server
ssh root@5.78.152.132

# 2. Install dependencies
apt update && apt upgrade -y
apt install -y python3 python3-pip nginx git certbot python3-certbot-nginx supervisor

# 3. Clone repos
mkdir -p /var/www/stripe-app && cd /var/www/stripe-app
git clone https://github.com/mohamederrajy/stripe-backend-.git backend
git clone https://github.com/mohamederrajy/stripe-front.git frontend

# 4. Install Python packages
cd /var/www/stripe-app/backend
pip3 install -r requirements.txt

# 5. Setup Supervisor
nano /etc/supervisor/conf.d/stripe-backend.conf
# (Copy content from DEPLOYMENT_GUIDE.md)
supervisorctl reread && supervisorctl update && supervisorctl start stripe-backend

# 6. Setup Nginx for API
nano /etc/nginx/sites-available/api.stripech.dev
# (Copy content from DEPLOYMENT_GUIDE.md)
ln -s /etc/nginx/sites-available/api.stripech.dev /etc/nginx/sites-enabled/

# 7. Setup Nginx for Frontend
nano /etc/nginx/sites-available/stripech.dev
# (Copy content from DEPLOYMENT_GUIDE.md)
ln -s /etc/nginx/sites-available/stripech.dev /etc/nginx/sites-enabled/

# 8. Update frontend API URL
nano /var/www/stripe-app/frontend/index.html
# Change: const API_URL = 'http://localhost:5001';
# To:     const API_URL = 'https://api.stripech.dev';

# 9. Set permissions
chown -R www-data:www-data /var/www/stripe-app
chmod -R 755 /var/www/stripe-app

# 10. Reload Nginx
nginx -t && systemctl reload nginx

# 11. Setup firewall
ufw allow 22/tcp && ufw allow 80/tcp && ufw allow 443/tcp
ufw enable

# 12. Get SSL certificates
certbot --nginx -d api.stripech.dev
certbot --nginx -d stripech.dev -d www.stripech.dev
```

---

## 🔄 Future Updates

When you push code to GitHub:

```bash
# Connect to server
ssh root@5.78.152.132

# Run update script
chmod +x /root/UPDATE_DEPLOY.sh
./UPDATE_DEPLOY.sh
```

Or manually:
```bash
cd /var/www/stripe-app/backend && git pull
supervisorctl restart stripe-backend

cd /var/www/stripe-app/frontend && git pull
```

---

## ✅ Verify Deployment

1. **Check Backend:**
   ```bash
   curl https://api.stripech.dev/health
   ```
   Should return: `{"status":"ok",...}`

2. **Check Frontend:**
   Open browser: https://stripech.dev

3. **Check Backend Status:**
   ```bash
   supervisorctl status stripe-backend
   ```

4. **View Logs:**
   ```bash
   tail -f /var/log/stripe-backend.out.log
   ```

---

## 🆘 If Something Goes Wrong

```bash
# Restart backend
supervisorctl restart stripe-backend

# Restart nginx
systemctl restart nginx

# Check what's running on port 5001
lsof -i :5001

# View error logs
tail -f /var/log/stripe-backend.err.log
tail -f /var/log/nginx/error.log
```

---

## 📞 DNS Checklist

Make sure these DNS records exist:

| Type | Name | Value |
|------|------|-------|
| A | stripech.dev | 5.78.152.132 |
| A | www.stripech.dev | 5.78.152.132 |
| A | api.stripech.dev | 5.78.152.132 |

Check DNS propagation: https://dnschecker.org

---

## 🎉 After Deployment

Your application will be live at:
- **Frontend:** https://stripech.dev
- **Backend API:** https://api.stripech.dev
- **API Health:** https://api.stripech.dev/health

Test the full workflow:
1. Visit https://stripech.dev
2. Enter Stripe API key
3. Configure settings
4. Charge customers!

---

## 📊 Monitoring

```bash
# Check backend service
systemctl status supervisor
supervisorctl status stripe-backend

# Check nginx
systemctl status nginx

# Monitor logs in real-time
tail -f /var/log/stripe-backend.out.log
tail -f /var/log/nginx/access.log
```

---

**Choose Option 1 (Automated) for fastest deployment! 🚀**

