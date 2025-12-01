# Quick Start - Charge All Customers at Once

This is the **simple script** to charge all your customers at the same time.

## 🚀 How to Use

### Step 1: Configure the Script

Open `charge_all_customers.py` and change these values at the top:

```python
# Amount to charge in DOLLARS (easy!)
CHARGE_AMOUNT_DOLLARS = 29.99  # CHANGE THIS

# Currency
CURRENCY = 'usd'  # or 'eur', 'gbp', etc.

# Description
CHARGE_DESCRIPTION = 'Monthly Subscription Fee'  # CHANGE THIS

# Set to True when ready to charge for real
LIVE_MODE = False  # Change to True to actually charge

# STRIPE RADAR PROTECTION (Important!)
MAX_CUSTOMERS_TO_CHARGE = 10   # Start with 10, then increase
DELAY_BETWEEN_CHARGES = 1.0    # 1 second between charges
```

**⚠️ For first time: Set `MAX_CUSTOMERS_TO_CHARGE = 10` to avoid Stripe Radar blocks!**

### Step 2: Set Your API Key

```bash
export STRIPE_SECRET_KEY='sk_test_your_key_here'
```

### Step 3: Test Run First

```bash
python charge_all_customers.py
```

This will show you:
- How many customers will be charged
- Who will be charged (names, emails)
- Total amount
- **No actual charges** (because LIVE_MODE = False)

### Step 4: Charge for Real

When you're ready:

1. Open `charge_all_customers.py`
2. Change `LIVE_MODE = False` to `LIVE_MODE = True`
3. Save the file
4. Run it:

```bash
python charge_all_customers.py
```

You'll need to type **YES** to confirm.

## 📊 What It Does

✅ Gets all your Stripe customers  
✅ Filters only customers with payment methods  
✅ Charges them all at once  
✅ Shows you progress in real-time  
✅ Saves results to a file  
✅ Handles errors automatically  

## 📝 Results

After running, you'll get a file like `charge_results_20241018_143022.txt` with:
- List of successful charges
- List of failed charges with error messages
- Total amount charged

## ⚠️ Important

- **Always test first** with `LIVE_MODE = False`
- Use **test API keys** for testing (`sk_test_...`)
- Use **live API keys** for real charges (`sk_live_...`)
- Make sure your customers have **agreed to recurring charges**

## 🛡️ Stripe Radar Protection

**Important for avoiding payment blocks:**

1. **First time:** Set `MAX_CUSTOMERS_TO_CHARGE = 10`
2. **After success:** Increase to 25, then 50, then remove limit (set to 0)
3. **Keep delay:** `DELAY_BETWEEN_CHARGES = 1.0` (at least 1 second)

**Why?** Stripe Radar can block batch charges that look suspicious. Starting small helps establish a pattern.

📖 **Read `STRIPE_RADAR_GUIDE.md` for detailed tips!**

## 🔄 When to Run

Run this script whenever you want to charge your customers:
- Monthly on the 1st
- Weekly on Mondays
- Whenever you want!

You can also set up a cron job to run it automatically.

## 💡 Example Cron Job (Monthly on 1st at 9am)

```bash
# Edit crontab
crontab -e

# Add this line:
0 9 1 * * cd /Users/aziz/Downloads/stripe-rebill && /usr/bin/python3 charge_all_customers.py
```

## 🆘 Troubleshooting

**"No customers found"**
- Make sure customers have payment methods saved
- Check you're using the right API key

**"Card declined"**
- Normal - some cards fail
- Customer needs to update their payment method
- Check the results file for details

**"Invalid API key"**
- Make sure STRIPE_SECRET_KEY is set
- Verify the key is correct in Stripe Dashboard

