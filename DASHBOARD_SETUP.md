# 🚀 Stripe Rebilling Dashboard - Setup Guide

Complete setup instructions for the web-based Stripe rebilling dashboard.

## 📋 What You Get

A beautiful web dashboard where you can:
- ✅ Configure all settings in a web interface
- ✅ Set Stripe API key, amount, currency, description
- ✅ Choose test or live mode
- ✅ Set customer limits and delays
- ✅ See real-time charging progress
- ✅ View success/failure results instantly
- ✅ No need to edit code!

---

## 🏗️ Architecture

```
React Frontend (Port 3000) → Flask Backend (Port 5000) → Stripe API
```

**Frontend (React):** Beautiful UI for configuration and results
**Backend (Flask/Python):** Secure server that handles Stripe API calls

---

## ⚡ Quick Start (3 Steps)

### Step 1: Install Backend Dependencies

```bash
cd /Users/aziz/Downloads/stripe-rebill/backend
pip3 install -r requirements.txt
```

### Step 2: Install Frontend Dependencies

```bash
cd /Users/aziz/Downloads/stripe-rebill/frontend
npm install
```

### Step 3: Start Both Servers

**Terminal 1 - Backend:**
```bash
cd /Users/aziz/Downloads/stripe-rebill/backend
python3 app.py
```

**Terminal 2 - Frontend:**
```bash
cd /Users/aziz/Downloads/stripe-rebill/frontend
npm start
```

### Step 4: Open Dashboard

Your browser should automatically open to:
**http://localhost:3000**

If not, open that URL manually.

---

## 📖 Detailed Setup Instructions

### Prerequisites

Make sure you have installed:
- ✅ **Python 3.7+** - Check: `python3 --version`
- ✅ **Node.js 14+** - Check: `node --version`
- ✅ **npm** - Check: `npm --version`

### Install Python (if needed)

**macOS:**
```bash
brew install python3
```

**Windows:**
Download from https://www.python.org/downloads/

### Install Node.js (if needed)

**macOS:**
```bash
brew install node
```

**Windows/Linux:**
Download from https://nodejs.org/

---

## 🔧 Backend Setup (Flask Server)

### 1. Navigate to Backend Directory

```bash
cd /Users/aziz/Downloads/stripe-rebill/backend
```

### 2. Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

This installs:
- Flask (web framework)
- Flask-CORS (allow frontend to connect)
- Stripe (Stripe API library)

### 3. Start Backend Server

```bash
python3 app.py
```

You should see:
```
🚀 Stripe Rebilling Dashboard - Backend Server
============================================================

Server starting on http://localhost:5000

Make sure to:
  1. Install dependencies: pip install flask flask-cors stripe
  2. Start React frontend on port 3000

============================================================

 * Running on http://localhost:5000
```

**Keep this terminal open!** Backend must stay running.

---

## 🎨 Frontend Setup (React Dashboard)

### 1. Navigate to Frontend Directory

**In a NEW terminal window:**

```bash
cd /Users/aziz/Downloads/stripe-rebill/frontend
```

### 2. Install Node Dependencies

```bash
npm install
```

This will take 1-2 minutes and install React and all dependencies.

### 3. Start Frontend Development Server

```bash
npm start
```

The browser will automatically open to **http://localhost:3000**

You should see the beautiful dashboard! 🎉

**Keep this terminal open too!** Frontend must stay running.

---

## 💻 Using the Dashboard

### 1. Enter Your Stripe API Key

- Get from: https://dashboard.stripe.com/apikeys
- For testing: Use **Test Mode** key (starts with `sk_test_`)
- For production: Use **Live Mode** key (starts with `sk_live_`)

Paste the key in the dashboard and click away from the field. You'll see:
- ✅ Green badge: "Valid (test mode)" or "Valid (live mode)"
- ❌ Red badge: "Invalid" - check your key

### 2. Configure Settings

All settings are in the left panel:

**Charge Amount:** How much to charge (in dollars)
- Example: `29.99` for $29.99

**Currency:** What currency to use
- Options: USD, EUR, GBP, CAD, AUD

**Charge Description:** What shows on customer's statement
- Example: "Monthly Subscription Fee"

**Live Mode:** Toggle between test and live
- 🟢 **OFF** (Test Mode): No real charges, simulation only
- 🔴 **ON** (Live Mode): Real charges, real money!

**Max Customers:** Limit how many to charge
- `10` = charge only first 10 customers
- `0` = charge ALL customers

**Delay Between Charges:** Seconds between each charge
- `1.0` = 1 second (recommended)
- `0.3` = faster but may trigger Stripe Radar

### 3. Check Customer Count (Optional)

Click **"Check Customer Count"** to see:
- How many total customers you have
- How many have payment methods saved

### 4. Start Charging

Click the big **"💳 Start Charging"** button.

**If Test Mode:**
- Confirms: "This is TEST MODE. No real charges."
- Click OK

**If Live Mode:**
- Shows warning: "⚠️ WARNING: Real money!"
- Shows amount, customer count
- Must confirm to proceed

### 5. Watch Real-Time Progress

The right panel shows live updates:
- 📋 "Retrieving customers..."
- 🔍 "Checking payment methods..."
- ✓ Found X customers
- [1/10] Charging customer...
- ✓ Success or ✗ Failed for each

### 6. View Results

When complete, you'll see:
- ✅ **Successful:** Count of successful charges
- ❌ **Failed:** Count of failed charges
- 💰 **Total Charged:** Total amount charged

Results are color-coded:
- 🟢 Green = Success
- 🔴 Red = Failed
- 🔵 Blue = Status updates

---

## 🎯 Example Usage

### Testing (Safe - No Real Charges)

1. Enter **Test API key** (`sk_test_...`)
2. Set amount: `1.00` (just $1 for testing)
3. Keep **Live Mode OFF** (🟢 Test Mode)
4. Set Max Customers: `5` (limit to 5 for testing)
5. Click **Start Charging**
6. Watch the simulation run!

### Production (Real Charges)

1. Enter **Live API key** (`sk_live_...`)
2. Set amount: `29.99` (your real price)
3. Turn **Live Mode ON** (🔴 Live Mode)
4. Set Max Customers: `10` (start small!)
5. Set Delay: `1.0` (avoid Stripe Radar)
6. Click **Start Charging**
7. Confirm the warning
8. Watch real charges happen!

---

## 🛡️ Security Notes

### ✅ SAFE: API Key Handling

- ✅ API keys are **never stored** in browser
- ✅ API keys are **sent to your own backend** (not external)
- ✅ Backend runs on **your computer** (localhost)
- ✅ All requests go through **your secure backend**

### ⚠️ If You Deploy to Production Server

If you deploy this to a real server (not localhost):

1. **Use HTTPS** (SSL certificate required)
2. **Add authentication** (login system)
3. **Use environment variables** for API keys
4. **Add rate limiting** to prevent abuse
5. **Whitelist IP addresses** if possible

---

## 🔍 Troubleshooting

### Backend Won't Start

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
pip3 install flask flask-cors stripe
```

### Frontend Won't Start

**Error:** `npm: command not found`

**Solution:** Install Node.js from https://nodejs.org/

**Error:** Dependencies errors

**Solution:**
```bash
rm -rf node_modules package-lock.json
npm install
```

### Dashboard Won't Load

**Check:**
1. Backend running on port 5000? Look for "Running on http://localhost:5000"
2. Frontend running on port 3000? Should auto-open browser
3. Check browser console for errors (F12)

### "Network Error" in Dashboard

**Cause:** Backend not running or not reachable

**Solution:**
1. Make sure backend is running (`python3 app.py`)
2. Check backend terminal for errors
3. Try restarting backend

### API Key Shows "Invalid"

**Check:**
1. Key copied completely (very long string)
2. No extra spaces at start/end
3. Correct mode (test key starts with `sk_test_`, live with `sk_live_`)
4. Key is active in Stripe Dashboard

---

## 🚀 Production Deployment

To deploy to a real server:

### Option 1: DigitalOcean/AWS/Heroku

1. **Backend:** Deploy Flask app
2. **Frontend:** Build and deploy React app
3. **Environment:** Set `STRIPE_SECRET_KEY` environment variable
4. **HTTPS:** Use Let's Encrypt or Cloudflare
5. **Auth:** Add login system (not included)

### Option 2: Simple VPS

```bash
# Build frontend
cd frontend
npm run build

# Serve with Flask
# Copy build/ folder to backend/static/
# Update Flask to serve static files
```

---

## 📊 Features

### What Works

- ✅ Real-time progress updates
- ✅ Automatic payment method filtering (skips Link/Google Pay/Apple Pay)
- ✅ Test mode simulation
- ✅ Live mode real charging
- ✅ Customer count preview
- ✅ Configurable delays and limits
- ✅ Beautiful modern UI
- ✅ Mobile responsive

### Future Enhancements (Not Included)

- ⏳ User authentication/login
- ⏳ Database to store history
- ⏳ Scheduled/automated charging
- ⏳ Email notifications
- ⏳ Multi-user support
- ⏳ Charge history reports

---

## 🎉 You're Done!

You now have a fully functional web dashboard for Stripe rebilling!

**Two terminals running:**
1. Backend: `python3 app.py` (port 5000)
2. Frontend: `npm start` (port 3000)

**Access dashboard:**
http://localhost:3000

**Have fun charging your customers! 💳**

---

## 📞 Need Help?

Check:
1. Backend terminal for errors
2. Frontend terminal for errors
3. Browser console (F12) for errors
4. This guide's Troubleshooting section

Common issues are usually:
- Dependencies not installed
- Servers not running
- Wrong ports
- API key issues

