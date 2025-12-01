# 🚫 Payment Method Filtering

## Overview

This dashboard **AUTOMATICALLY SKIPS** the following payment methods:
- ✗ Link (Stripe's Link payment method)
- ✗ Google Pay
- ✗ Apple Pay

Only **regular card payments** are processed.

## Why Skip These Payment Methods?

1. **Link** - May have limitations or restrictions
2. **Google Pay** - Wallet-based, may need special handling
3. **Apple Pay** - Wallet-based, may need special handling

## How It Works

### During Customer Filtering:
The system checks ALL payment methods for each customer and:
1. Lists all payment methods (up to 10 per customer)
2. Skips any Link, Google Pay, or Apple Pay methods
3. Only accepts customers with regular card payment methods
4. Tracks how many special payment methods were skipped

### During Charging:
When actually charging customers, the system:
1. Retrieves all payment methods again
2. Finds the first valid card payment method (not Link/GPay/APay)
3. Uses that payment method for the charge
4. Skips the customer if only Link/GPay/APay methods exist

## Filtering Logic

```python
# Payment method is SKIPPED if:
- pm.type == 'link'
- pm.type == 'google_pay'
- pm.type == 'apple_pay'
- pm has 'link' attribute set to True
- pm.card.wallet.type is 'google_pay', 'apple_pay', or 'link'
```

## What You'll See

After charging, you'll see:
- ✅ Number of successful charges
- ❌ Number of failed charges
- 🚫 Number of Link/GPay/APay payment methods skipped

## This is FORCED - You Cannot Disable It

The payment method filtering is **hardcoded** and cannot be turned off. This ensures:
- Consistent charging behavior
- No accidental charges to incompatible payment methods
- Protection against payment method issues

## Example

If you have 100 customers:
- 80 with regular cards → Will be charged
- 10 with Link only → Will be skipped
- 10 with Google Pay only → Will be skipped

Result: 80 customers charged, 20 skipped

## Questions?

The filtering happens automatically in:
- `backend/server.py` - `/charge` endpoint
- Filter applied twice: once when finding customers, once when charging
- No configuration needed - works out of the box!
