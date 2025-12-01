# How to Set Up Your Stripe API Key

You only need **ONE thing** to run the script: Your Stripe Secret API Key

## 🔑 Step 1: Get Your API Key from Stripe

### Go to Stripe Dashboard:
👉 **https://dashboard.stripe.com/apikeys**

### Copy Your Secret Key:

**For Testing (Recommended First):**
- Make sure you're in **Test mode** (toggle at top of dashboard)
- Find **"Secret key"** section
- Click **"Reveal test key"**
- Copy the key (starts with `sk_test_...`)

**For Production (After Testing):**
- Switch to **Live mode**
- Find **"Secret key"** section
- Copy the key (starts with `sk_live_...`)

---

## 🔧 Step 2: Set the API Key

Choose ONE of these methods:

### Method A: Terminal Command (Easiest)

Open Terminal and run:

```bash
export STRIPE_SECRET_KEY='sk_test_your_actual_key_here'
```

**Replace** `sk_test_your_actual_key_here` with your real key!

**Example:**
```bash
export STRIPE_SECRET_KEY='sk_test_51ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh1234567890'
```

**Note:** This only works for current terminal session. If you close terminal, you'll need to run it again.

---

### Method B: .env File (Permanent)

1. Create a file named `.env` in the stripe-rebill folder:
   ```bash
   cd /Users/aziz/Downloads/stripe-rebill
   nano .env
   ```

2. Add this line:
   ```
   STRIPE_SECRET_KEY=sk_test_your_actual_key_here
   ```

3. Save the file (Ctrl+O, Enter, Ctrl+X in nano)

4. Update the script to use .env:
   ```bash
   pip install python-dotenv
   ```

**Example .env file:**
```
STRIPE_SECRET_KEY=sk_test_51ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh1234567890
```

---

### Method C: Add to Shell Profile (Always Available)

For permanent setup across all terminal sessions:

1. Open your shell profile:
   ```bash
   nano ~/.zshrc
   ```

2. Add this line at the end:
   ```bash
   export STRIPE_SECRET_KEY='sk_test_your_actual_key_here'
   ```

3. Save and reload:
   ```bash
   source ~/.zshrc
   ```

---

## ✅ Step 3: Verify It's Set

Check if your API key is set correctly:

```bash
echo $STRIPE_SECRET_KEY
```

You should see your key printed out.

---

## 🚀 Step 4: Run the Script

Now you can run:

```bash
python3 charge_all_customers.py
```

---

## 📋 Quick Reference

| Mode | Key Starts With | Use For |
|------|----------------|---------|
| **Test** | `sk_test_...` | Testing (no real charges) |
| **Live** | `sk_live_...` | Production (real charges) |

---

## ⚠️ Security Tips

1. **Never share your secret key** with anyone
2. **Never commit it to git** (.env is in .gitignore)
3. **Use test keys first** to verify everything works
4. **Rotate keys regularly** in Stripe Dashboard

---

## 🆘 Troubleshooting

### "ERROR: Please set STRIPE_SECRET_KEY environment variable"

Your API key is not set. Try:

```bash
# Check if it's set
echo $STRIPE_SECRET_KEY

# If empty, set it
export STRIPE_SECRET_KEY='sk_test_your_key_here'
```

### "Invalid API key"

- Check you copied the entire key
- Make sure there are no extra spaces
- Verify the key in Stripe Dashboard is active
- For test mode, use `sk_test_...` key
- For live mode, use `sk_live_...` key

### "No such customer"

- Make sure you're using the right mode (test vs live)
- Test keys only work with test customers
- Live keys only work with live customers

---

## 🎯 Complete Example

```bash
# 1. Get your test key from Stripe Dashboard
# 2. Set it in terminal
export STRIPE_SECRET_KEY='sk_test_51ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh1234567890'

# 3. Verify it's set
echo $STRIPE_SECRET_KEY

# 4. Run the script
python3 charge_all_customers.py
```

That's it! No customer IDs or other configuration needed. The script automatically finds all your customers and charges them.

