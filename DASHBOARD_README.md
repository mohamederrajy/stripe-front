# 💳 Stripe Rebilling Dashboard

**Beautiful web interface to batch charge your Stripe subscription customers!**

![Dashboard Preview](https://via.placeholder.com/800x400/667eea/ffffff?text=Stripe+Rebilling+Dashboard)

---

## ⚡ Super Quick Start

```bash
# 1. Go to project folder
cd /Users/aziz/Downloads/stripe-rebill

# 2. Run the start script (installs everything and starts servers)
./start_dashboard.sh
```

Your browser will open to **http://localhost:3000** automatically!

---

## 📖 Manual Start (If Script Doesn't Work)

### Terminal 1 - Backend:
```bash
cd /Users/aziz/Downloads/stripe-rebill/backend
pip3 install -r requirements.txt
python3 app.py
```

### Terminal 2 - Frontend:
```bash
cd /Users/aziz/Downloads/stripe-rebill/frontend
npm install
npm start
```

---

## ✨ Features

### Configuration (Left Panel)

All settings customizable through web UI:

- **💳 Stripe API Key** - Your secret key (test or live)
- **💰 Charge Amount** - How much to charge (in dollars)
- **💱 Currency** - USD, EUR, GBP, CAD, AUD
- **📝 Description** - What shows on customer statement
- **🔴/🟢 Live/Test Mode** - Toggle between real and simulation
- **👥 Max Customers** - Limit how many to charge (0 = all)
- **⏱️ Delay** - Seconds between charges (anti-Radar)

### Real-Time Progress (Right Panel)

Watch live as it:
- 📋 Retrieves customers
- 🔍 Checks payment methods
- ⚡ Charges each customer
- ✅ Shows successes
- ❌ Shows failures
- 💰 Displays total charged

### Smart Features

- ✅ **Automatic filtering** - Skips Link, Google Pay, Apple Pay
- ✅ **Real-time updates** - See each charge as it happens
- ✅ **Test mode** - Safe simulation before real charges
- ✅ **Validation** - Checks API key before starting
- ✅ **Customer preview** - See count before charging
- ✅ **Beautiful UI** - Modern, responsive design
- ✅ **Progress tracking** - Never lose track of what's happening

---

## 🎯 How to Use

### 1. Get Your Stripe API Key

Visit: https://dashboard.stripe.com/apikeys

- **For Testing:** Copy the **Secret key** from **Test mode**
- **For Production:** Copy the **Secret key** from **Live mode**

### 2. Open Dashboard

Go to: **http://localhost:3000**

### 3. Configure Settings

- Paste your Stripe API key (it will validate automatically)
- Set the amount to charge
- Choose currency
- Enter description
- Toggle Live Mode (OFF for testing, ON for real charges)
- Set max customers (start with 10 for first run)
- Set delay (1.0 second recommended)

### 4. Preview (Optional)

Click **"Check Customer Count"** to see how many customers will be charged.

### 5. Start Charging

Click **"💳 Start Charging"**

- Confirm the prompt
- Watch real-time progress
- See results when complete

### 6. Review Results

- ✅ Green = Successful charges
- ❌ Red = Failed charges (with error messages)
- 💰 Total amount charged

---

## 🛡️ Safety Features

### Test Mode First!

Always test with **Test Mode** before using **Live Mode**:

1. Use **test API key** (`sk_test_...`)
2. Keep **Live Mode toggle OFF** (🟢 green)
3. Run the charging process
4. Verify everything works
5. **Then** switch to Live Mode with live API key

### Progressive Rollout

Start small and increase gradually:

1. **First run:** 10 customers, 1.0s delay
2. **Second run:** 25 customers, 1.0s delay
3. **Third run:** 50 customers, 0.5s delay
4. **Later runs:** All customers, 0.3s delay

This avoids Stripe Radar blocks!

### Smart Filtering

Automatically skips customers with:
- 🔗 Link payments
- 📱 Google Pay
- 🍎 Apple Pay

Only charges customers with regular credit/debit cards.

---

## 🚀 Architecture

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   React     │────────▶│   Flask     │────────▶│   Stripe    │
│  Frontend   │         │   Backend   │         │     API     │
│  (Port 3000)│◀────────│  (Port 5000)│◀────────│             │
└─────────────┘         └─────────────┘         └─────────────┘
```

**Why Backend Needed:**
- ✅ Keeps API keys secure (never in browser)
- ✅ Handles actual Stripe API calls
- ✅ Provides real-time progress streaming
- ✅ Processes charges server-side

---

## 💻 Tech Stack

### Frontend
- **React 18** - Modern UI framework
- **Axios** - HTTP requests
- **CSS3** - Beautiful gradient design
- **Server-Sent Events** - Real-time updates

### Backend
- **Flask** - Python web framework
- **Stripe Python SDK** - Stripe API integration
- **Flask-CORS** - Cross-origin support
- **Threading** - Background processing

---

## 📊 What's Customizable in UI

Everything! No code editing needed:

| Setting | What It Does | Example Values |
|---------|--------------|----------------|
| **API Key** | Your Stripe secret key | `sk_test_...` or `sk_live_...` |
| **Amount** | Charge amount in dollars | `29.99`, `50.00`, `199.99` |
| **Currency** | Currency code | `usd`, `eur`, `gbp`, `cad`, `aud` |
| **Description** | Shows on customer statement | `Monthly Subscription - Nov 2024` |
| **Live Mode** | Test vs Real charges | ON (🔴) or OFF (🟢) |
| **Max Customers** | Limit how many to charge | `10`, `50`, `100`, `0` (all) |
| **Delay** | Seconds between charges | `0.3`, `1.0`, `2.0` |

---

## 🎨 Screenshots

### Configuration Panel
- Enter all settings
- Validate API key
- Check customer count
- Start charging button

### Progress Panel
- Real-time charging updates
- Color-coded results
- Success/failure tracking
- Summary statistics

---

## 🆘 Troubleshooting

### Can't Access Dashboard

**Problem:** Browser shows "Can't reach localhost:3000"

**Solution:**
1. Make sure frontend is running: `npm start` in frontend folder
2. Check terminal for errors
3. Try `http://127.0.0.1:3000` instead

### API Key Shows "Invalid"

**Problem:** Red "Invalid" badge after entering key

**Solution:**
1. Make sure you copied the **entire key** (very long)
2. No spaces before/after the key
3. Using **Secret key**, not Publishable key
4. Key is from correct mode (test vs live)
5. Backend server is running

### "Network Error" When Charging

**Problem:** Error message when clicking Start Charging

**Solution:**
1. Backend must be running on port 5000
2. Check backend terminal for errors
3. Try restarting backend: `python3 app.py`

### No Real-Time Updates

**Problem:** Charging starts but no progress shows

**Solution:**
1. Check browser console for errors (F12)
2. Make sure using modern browser (Chrome, Firefox, Safari)
3. Restart both servers

---

## 🎉 Quick Tips

### Testing
- Always use **Test Mode** first
- Use test API key: `sk_test_...`
- Start with small amounts: `$1.00`
- Limit to 5-10 customers initially

### Production
- Switch to **Live Mode** carefully
- Use live API key: `sk_live_...`
- Start with 10 customers max
- Use 1.0 second delay minimum
- Monitor Stripe Dashboard

### Best Practices
- ✅ Test before each production run
- ✅ Start with small batches
- ✅ Increase gradually over time
- ✅ Keep delay at 1.0s minimum
- ✅ Monitor results in real-time

---

## 📚 Documentation

- **Full Setup Guide:** `DASHBOARD_SETUP.md`
- **Command Line Script:** `charge_all_customers.py`
- **Backend API:** `backend/app.py`
- **Frontend App:** `frontend/src/App.js`

---

## 🌟 That's It!

You now have a professional web dashboard for Stripe rebilling!

**Start it:**
```bash
./start_dashboard.sh
```

**Access it:**
http://localhost:3000

**Have fun charging! 💳**

