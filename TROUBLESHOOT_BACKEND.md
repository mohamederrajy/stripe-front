# 🔧 Backend Crash Troubleshooting

## Error: "FATAL - Exited too quickly"

This means the backend is crashing immediately after starting.

---

## Step 1: Check the Error Logs

```bash
# View error logs
tail -50 /var/log/stripe-backend.err.log

# View output logs
tail -50 /var/log/stripe-backend.out.log
```

Look for error messages!

---

## Step 2: Test Backend Manually

```bash
# Go to backend directory
cd /var/www/stripe-app/backend

# Try running manually
python3 server.py
```

This will show the exact error!

---

## Common Issues & Solutions

### Issue 1: Port 5001 Already in Use

**Error:** `Address already in use` or `Port 5001 is in use`

**Solution:**
```bash
# Kill process on port 5001
lsof -ti:5001 | xargs kill -9

# Or find and kill manually
lsof -i :5001
kill -9 [PID]

# Restart backend
supervisorctl restart stripe-backend
```

### Issue 2: Missing Python Packages

**Error:** `ModuleNotFoundError: No module named 'flask'` or `'stripe'`

**Solution:**
```bash
cd /var/www/stripe-app/backend
pip3 install -r requirements.txt

# Or install individually
pip3 install flask stripe

# Restart backend
supervisorctl restart stripe-backend
```

### Issue 3: Wrong Python Path

**Error:** Backend can't find Python modules

**Solution:**
```bash
# Find Python path
which python3

# Update supervisor config
nano /etc/supervisor/conf.d/stripe-backend.conf
```

Change the command line to use full path:
```ini
command=/usr/bin/python3 /var/www/stripe-app/backend/server.py
```

Then:
```bash
supervisorctl reread
supervisorctl update
supervisorctl restart stripe-backend
```

### Issue 4: Permission Issues

**Error:** `Permission denied`

**Solution:**
```bash
# Fix ownership
chown -R www-data:www-data /var/www/stripe-app

# Fix permissions
chmod -R 755 /var/www/stripe-app

# Make server.py executable
chmod +x /var/www/stripe-app/backend/server.py

# Restart
supervisorctl restart stripe-backend
```

### Issue 5: File Not Found

**Error:** `No such file or directory`

**Solution:**
```bash
# Check if files exist
ls -la /var/www/stripe-app/backend/

# If backend folder is missing, clone again
cd /var/www/stripe-app
git clone https://github.com/mohamederrajy/stripe-backend-.git backend
cd backend
pip3 install -r requirements.txt

# Restart
supervisorctl restart stripe-backend
```

### Issue 6: Wrong Port Configuration

**Error:** Backend trying to bind to wrong port

**Solution:**
```bash
# Check if server.py uses port 5001
grep -n "port" /var/www/stripe-app/backend/server.py

# Should see: app.run(host='0.0.0.0', port=5001, debug=True)
```

---

## Step 3: Check Supervisor Configuration

```bash
# View supervisor config
cat /etc/supervisor/conf.d/stripe-backend.conf

# Should look like this:
# [program:stripe-backend]
# directory=/var/www/stripe-app/backend
# command=/usr/bin/python3 server.py
# user=www-data
# autostart=true
# autorestart=true
# stderr_logfile=/var/log/stripe-backend.err.log
# stdout_logfile=/var/log/stripe-backend.out.log
# environment=PYTHONUNBUFFERED="1"
```

If config is wrong, fix it:
```bash
nano /etc/supervisor/conf.d/stripe-backend.conf
```

Then:
```bash
supervisorctl reread
supervisorctl update
supervisorctl restart stripe-backend
```

---

## Step 4: Check System Resources

```bash
# Check if server has enough memory
free -h

# Check disk space
df -h

# Check if port is accessible
netstat -tulpn | grep 5001
```

---

## Quick Fix Commands (Run These)

```bash
# 1. Kill any process on port 5001
lsof -ti:5001 | xargs kill -9 2>/dev/null

# 2. Go to backend directory
cd /var/www/stripe-app/backend

# 3. Install dependencies
pip3 install flask stripe

# 4. Fix permissions
chown -R www-data:www-data /var/www/stripe-app
chmod +x /var/www/stripe-app/backend/server.py

# 5. Test manually first
python3 server.py
# Press Ctrl+C after confirming it works

# 6. Restart supervisor
supervisorctl restart stripe-backend

# 7. Check status
supervisorctl status stripe-backend
```

---

## Step 5: Run Backend Without Supervisor (Debug Mode)

```bash
cd /var/www/stripe-app/backend
python3 server.py
```

Leave it running and test:
```bash
# In another terminal
curl http://localhost:5001/health
```

If this works, the issue is with supervisor configuration.

---

## Step 6: Alternative Supervisor Config

If still not working, try this config:

```bash
nano /etc/supervisor/conf.d/stripe-backend.conf
```

Replace with:
```ini
[program:stripe-backend]
directory=/var/www/stripe-app/backend
command=/usr/bin/python3 /var/www/stripe-app/backend/server.py
user=root
autostart=true
autorestart=true
stderr_logfile=/var/log/stripe-backend.err.log
stdout_logfile=/var/log/stripe-backend.out.log
environment=PYTHONUNBUFFERED="1",PATH="/usr/bin:/bin"
stopasgroup=true
killasgroup=true
```

Then:
```bash
supervisorctl reread
supervisorctl update
supervisorctl restart stripe-backend
supervisorctl status stripe-backend
```

---

## Step 7: Check Nginx Configuration

```bash
# Test nginx config
nginx -t

# If errors, view config
cat /etc/nginx/sites-available/api.stripech.dev

# Reload nginx
systemctl reload nginx
```

---

## Step 8: View All Logs in Real-Time

```bash
# Watch logs as they happen
tail -f /var/log/stripe-backend.err.log /var/log/stripe-backend.out.log
```

Then in another terminal:
```bash
supervisorctl restart stripe-backend
```

Watch what error appears!

---

## ✅ Success Checklist

Backend is working when you see:

```bash
supervisorctl status stripe-backend
# Should show: RUNNING    pid 12345, uptime 0:00:05

curl http://localhost:5001/health
# Should return: {"status":"ok","message":"Backend is running",...}
```

---

## 🆘 Still Not Working?

Send me the output of these commands:

```bash
# 1. Error logs
tail -50 /var/log/stripe-backend.err.log

# 2. Output logs  
tail -50 /var/log/stripe-backend.out.log

# 3. Manual test
cd /var/www/stripe-app/backend
python3 server.py

# 4. Supervisor config
cat /etc/supervisor/conf.d/stripe-backend.conf

# 5. Check if backend files exist
ls -la /var/www/stripe-app/backend/
```

