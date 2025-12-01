# Fix: "No valid payment method types" Error

## The Problem

You're seeing this error:
```
No valid payment method types for this Payment Intent. 
Please ensure that you have activated payment methods compatible 
with your chosen currency in your dashboard
```

This means **card payments aren't enabled in your Stripe account** for your currency.

---

## ✅ Solution: Enable Card Payments in Stripe Dashboard

### Step 1: Go to Payment Methods Settings

Visit: **https://dashboard.stripe.com/settings/payment_methods**

### Step 2: Enable Cards

1. Look for **"Cards"** in the list of payment methods
2. **Turn it ON** (should show as enabled/active)
3. Make sure it's enabled for **USD** (or whatever currency you're using)

### Step 3: Check Your Country/Region

1. In the same page, verify your account country is correct
2. Make sure card payments are available in your region
3. Some countries have restrictions - check Stripe's supported countries

### Step 4: Save and Wait

1. Click **Save** if there's a save button
2. Wait **1-2 minutes** for changes to propagate
3. Try running the script again

---

## 🔍 Alternative Check: Verify Your Currency

Your script is set to charge in **USD**. Make sure:

1. Card payments are enabled for USD
2. Your Stripe account supports USD
3. If you're in a different country, you might need to:
   - Use your local currency instead
   - Or enable multi-currency support

### To Change Currency:

Edit `charge_all_customers.py`:

```python
# Change this if you need a different currency
CURRENCY = 'usd'  # Change to 'eur', 'gbp', etc.
```

---

## 🌍 Common Currency Codes

| Country | Currency Code |
|---------|---------------|
| USA | `usd` |
| UK | `gbp` |
| Europe | `eur` |
| Canada | `cad` |
| Australia | `aud` |

---

## 📋 Checklist

- [ ] Go to https://dashboard.stripe.com/settings/payment_methods
- [ ] Enable "Cards" payment method
- [ ] Verify currency is supported (USD, EUR, GBP, etc.)
- [ ] Save changes
- [ ] Wait 1-2 minutes
- [ ] Run the script again

---

## 🆘 Still Not Working?

### Check if you're in Test Mode vs Live Mode

1. Look at the top of your Stripe Dashboard
2. Toggle between **Test mode** and **Live mode**
3. Enable card payments in BOTH modes if needed

### Contact Stripe Support

If card payments still don't work:

1. Go to https://support.stripe.com
2. Explain: "I can't enable card payments for USD"
3. They'll help verify your account is fully activated

---

## 🔄 After Enabling Card Payments

Run the script again:

```bash
python3 charge_all_customers.py
```

It should work now! ✅

---

## ⚠️ Important Note

The script has been updated to work better with different Stripe configurations. Make sure you have the latest version.

If customers have old payment methods saved as "sources" (older Stripe API), the script will now try that method too.


