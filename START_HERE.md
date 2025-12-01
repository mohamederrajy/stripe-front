# 🚀 Stripe Rebilling Dashboard - Quick Start Guide

## What This Does

This dashboard allows you to charge all your existing Stripe customers at once. Perfect for subscription services where you want to rebill customers on demand.

## 📋 Requirements

- Python 3.7 or higher
- Stripe account with API keys
- Customers in your Stripe account

## 🎯 Step-by-Step Setup

### Step 1: Install Dependencies

Open Terminal and run:

```bash
cd /Users/aziz/Downloads/stripe-rebill/backend
pip3 install -r requirements.txt
```

### Step 2: Start the Backend Server

In the same terminal:

```bash
python3 server.py
```

You should see:
```
🚀 Stripe Rebilling Backend Server
✅ CORS enabled for all origins
🌐 Server running at: http://localhost:5000
```

**Keep this terminal open!** The backend must stay running.

### Step 3: Start the Frontend

Open a **NEW terminal** window and run:

```bash
cd /Users/aziz/Downloads/stripe-rebill/frontend
python3 -m http.server 8000
```

You should see:
```
Serving HTTP on :: port 8000 (http://[::]:8000/) ...
```

### Step 4: Open the Dashboard

Open your web browser and go to:

**http://localhost:8000**

## 🎨 Using the Dashboard

### 1. Enter Your Stripe API Key

- Get your API key from: https://dashboard.stripe.com/apikeys
- For testing: Use keys starting with `sk_test_`
- For real charges: Use keys starting with `sk_live_`

### 2. Configure Charge Settings

- **Amount**: How much to charge (in dollars)
- **Currency**: USD, EUR, GBP, etc.
- **Description**: What the charge is for
- **Max Customers**: Limit how many to charge (0 = all)
- **Delay**: Time between charges (helps avoid Stripe Radar blocks)
- **Skip Special Payments**: Skip Link/Google Pay/Apple Pay (recommended)

### 3. Start Charging

Click the "Start Charging Customers" button and watch the progress!

## ⚙️ Important Settings

### For Testing (Recommended First Time)
- Use **Test Mode** API key (`sk_test_...`)
- Set **Max Customers** to `5` or `10`
- Set **Delay** to `1.0` seconds
- Use a small **Amount** like `1.00`

### For Production
- Use **Live Mode** API key (`sk_live_...`)
- Start with **Max Customers** at `10-20`
- Keep **Delay** at `1.0` seconds or higher
- After successful runs, increase gradually

## 🛡️ Stripe Radar Protection

Stripe Radar monitors unusual activity. To avoid blocks:

1. **Start Small**: Charge 10-20 customers first
2. **Use Delays**: Keep 1-2 second delays between charges
3. **Increase Gradually**: If successful, charge more customers next time
4. **Monitor**: Check Stripe Dashboard for any flags

## 🔐 Security Notes

- ✅ Your API key is sent securely to the backend only
- ✅ Never stored in browser or logs
- ✅ Backend runs on your local machine only
- ✅ No data sent to external servers

## ❓ Troubleshooting

### "Cannot connect to backend"
- Make sure `python3 server.py` is running in backend directory
- Check that no other app is using port 5000

### "No customers found with payment methods"
- Verify customers exist in your Stripe Dashboard
- Ensure customers have valid payment methods attached
- Check you're using the correct API key (test vs live)

### "Invalid API key"
- Get fresh API key from Stripe Dashboard
- Make sure to copy the entire key
- Check for extra spaces before/after the key

### Charges Failing
- Enable "Cards" payment method in Stripe Dashboard
- Check customer payment methods are valid
- Try with smaller amounts first
- Review Stripe Dashboard for specific errors

## 🎯 Common Use Cases

### Monthly Subscription Rebill
```
Amount: 29.99
Currency: USD
Description: Monthly Subscription Fee
Max Customers: 0 (all)
Delay: 1.0
```

### One-Time Special Charge
```
Amount: 9.99
Currency: USD
Description: Special Feature Access
Max Customers: 0 (all)
Delay: 1.0
```

### Gradual Rollout
```
Amount: 49.99
Currency: USD
Description: Premium Upgrade
Max Customers: 20 (test batch)
Delay: 2.0
```

## 📊 Understanding Results

After charging completes, you'll see:
- **Successful**: Charges that went through
- **Failed**: Charges that were declined or errored
- **Detailed list**: Each customer with status and error messages

Failed charges might be due to:
- Insufficient funds
- Expired cards
- Card issuer declined
- Payment method removed

## 🔄 Next Steps

1. **Test first** with small amounts in test mode
2. **Review results** carefully
3. **Switch to live mode** when ready
4. **Monitor Stripe Dashboard** for any issues
5. **Adjust settings** based on results

## 💡 Pro Tips

- Always test in **Test Mode** first
- Start with **small batches** (10-20 customers)
- Use appropriate **delays** (1-2 seconds)
- Keep **descriptions clear** for customer clarity
- Check **Stripe Dashboard** regularly
- Save failed customer list for follow-up

## 📞 Need Help?

- **Stripe Dashboard**: https://dashboard.stripe.com
- **Stripe Docs**: https://stripe.com/docs
- **API Keys**: https://dashboard.stripe.com/apikeys
- **Payment Methods**: https://dashboard.stripe.com/settings/payment_methods

---

**Ready to start?** Open two terminals, start both servers, and go to http://localhost:8000! 🚀

