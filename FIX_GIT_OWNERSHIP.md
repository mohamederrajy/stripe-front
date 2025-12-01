# 🔧 Fix Git Ownership on Server

## Quick Fix (Copy/Paste):

```bash
# Fix ownership for both backend and frontend
chown -R root:root /var/www/stripe-app/backend
chown -R root:root /var/www/stripe-app/frontend

# Now pull updates
cd /var/www/stripe-app/backend && git pull origin main
cd /var/www/stripe-app/frontend && git pull origin main

# Restart backend
supervisorctl restart stripe-backend
supervisorctl status stripe-backend
```

---

## ✅ All Done!

Now test: **https://stripech.dev** - should load SUPER FAST! ⚡️

