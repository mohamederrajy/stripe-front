# Stripe Radar Protection Guide

## What is Stripe Radar?

Stripe Radar is Stripe's built-in fraud detection system. It monitors all charges and can **block or flag suspicious payments** to protect you and your customers.

## Why Might Radar Block Your Charges?

When you charge many customers at once, Radar might see it as suspicious because:

1. ❌ **Sudden batch charging** - Many charges in a short time
2. ❌ **Unusual pattern** - Different from your normal charging behavior
3. ❌ **High velocity** - Too many transactions too quickly
4. ❌ **New account** - If your Stripe account is new

## ✅ How to Avoid Radar Blocks

### 1. **Start Small (IMPORTANT!)**

The script now has built-in protection. Configure in `charge_all_customers.py`:

```python
# First time: Charge only 5-10 customers
MAX_CUSTOMERS_TO_CHARGE = 10

# After successful run: Increase gradually
MAX_CUSTOMERS_TO_CHARGE = 25

# When confident: Remove limit (charge all)
MAX_CUSTOMERS_TO_CHARGE = 0
```

### 2. **Add Delays Between Charges**

```python
# 1 second between charges (recommended)
DELAY_BETWEEN_CHARGES = 1.0

# For large batches: Use 2-3 seconds
DELAY_BETWEEN_CHARGES = 2.0
```

### 3. **Use Proper Descriptions**

```python
# Good - Clear and descriptive
CHARGE_DESCRIPTION = 'Monthly Subscription - November 2024'

# Bad - Vague or suspicious
CHARGE_DESCRIPTION = 'Payment'  # ❌ Too vague
```

### 4. **Gradual Rollout Strategy**

**Week 1:** Charge 10 customers
```python
MAX_CUSTOMERS_TO_CHARGE = 10
DELAY_BETWEEN_CHARGES = 2.0
```

**Week 2:** Charge 25 customers
```python
MAX_CUSTOMERS_TO_CHARGE = 25
DELAY_BETWEEN_CHARGES = 1.5
```

**Week 3:** Charge 50 customers
```python
MAX_CUSTOMERS_TO_CHARGE = 50
DELAY_BETWEEN_CHARGES = 1.0
```

**Week 4+:** Charge all customers
```python
MAX_CUSTOMERS_TO_CHARGE = 0  # No limit
DELAY_BETWEEN_CHARGES = 1.0
```

## 📞 Contact Stripe Support (Recommended)

**Before running large batches, notify Stripe:**

1. Go to https://dashboard.stripe.com/support
2. Tell them:
   - "I'm running a subscription service"
   - "I'll be charging [X] customers on [date]"
   - "Each charge will be $[amount] for monthly subscriptions"
   - "Customers have agreed to recurring charges"

This helps Stripe whitelist your batch charging!

## ⚠️ What If Charges Get Blocked?

### Signs of Radar Blocking:

- Charges fail with "declined" messages
- Stripe dashboard shows "blocked by Radar"
- Multiple legitimate cards getting declined

### Solutions:

1. **Check Stripe Dashboard**
   - Go to https://dashboard.stripe.com/radar/overview
   - Review blocked charges
   - Unblock false positives

2. **Adjust Radar Rules**
   - Dashboard → Radar → Rules
   - Review and adjust sensitivity
   - Whitelist your subscription charges

3. **Contact Stripe Support**
   - Explain your legitimate use case
   - Request review of blocked charges
   - Ask to adjust Radar settings

## 📋 Best Practices Checklist

Before running batch charges:

- [ ] Set `MAX_CUSTOMERS_TO_CHARGE` to small number (5-10) for first run
- [ ] Set `DELAY_BETWEEN_CHARGES` to at least 1.0 second
- [ ] Use clear, descriptive charge descriptions
- [ ] Run in TEST MODE first
- [ ] Verify customers have agreed to recurring charges
- [ ] Consider notifying Stripe Support beforehand
- [ ] Monitor Stripe Dashboard during charging
- [ ] Gradually increase batch size over time

## 🔒 Additional Security Tips

1. **Use Subscriptions API** (Alternative)
   - Instead of one-time charges, use Stripe Subscriptions
   - Radar is more lenient with subscription renewals
   - Consider `stripe_rebilling.py` for subscription management

2. **Verify Customer Information**
   - Ensure customer emails are valid
   - Verify payment methods are active
   - Check billing addresses are complete

3. **Set Up Webhooks**
   - Monitor for failed charges in real-time
   - Get notified of Radar blocks
   - Automate retry logic

## Example Configuration for Safety

```python
# ============================================
# SAFE CONFIGURATION FOR FIRST TIME
# ============================================

CHARGE_AMOUNT_DOLLARS = 29.99
CURRENCY = 'usd'
CHARGE_DESCRIPTION = 'Premium Monthly Subscription - November 2024'
LIVE_MODE = False  # Test first!

# Stripe Radar Protection
MAX_CUSTOMERS_TO_CHARGE = 10    # Start with just 10
DELAY_BETWEEN_CHARGES = 2.0     # 2 seconds between each

# ============================================
```

## Monitoring During Batch Charging

1. **Watch Stripe Dashboard**
   - Open: https://dashboard.stripe.com/payments
   - Monitor charges in real-time
   - Check for blocks or failures

2. **Review the Script Output**
   - Watch for card errors vs. Radar blocks
   - Check success/failure ratio
   - Review the results file after completion

3. **Check Radar Overview**
   - Dashboard → Radar → Overview
   - Look for unusual spikes in blocks
   - Review risk scores

## When Everything is Working Well

Once you've successfully charged customers several times:

```python
# After 3-4 successful batch runs, you can:
MAX_CUSTOMERS_TO_CHARGE = 0     # Remove limit
DELAY_BETWEEN_CHARGES = 1.0     # Keep some delay for safety
```

## Need Help?

- **Stripe Documentation**: https://stripe.com/docs/radar
- **Stripe Support**: https://support.stripe.com
- **Stripe Dashboard**: https://dashboard.stripe.com/radar

Remember: It's better to be safe and start slow than to have all charges blocked! 🛡️

