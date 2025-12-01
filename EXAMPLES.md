# Configuration Examples

## Example 1: Monthly $29.99 Subscription

```python
# In charge_all_customers.py
CHARGE_AMOUNT_DOLLARS = 29.99
CURRENCY = 'usd'
CHARGE_DESCRIPTION = 'Premium Monthly Subscription - November 2024'
LIVE_MODE = False  # Set to True when ready
```

## Example 2: Weekly $9.99 Payment

```python
# In charge_all_customers.py
CHARGE_AMOUNT_DOLLARS = 9.99
CURRENCY = 'usd'
CHARGE_DESCRIPTION = 'Weekly Access Fee'
LIVE_MODE = False
```

## Example 3: Annual $199 Subscription

```python
# In charge_all_customers.py
CHARGE_AMOUNT_DOLLARS = 199.00
CURRENCY = 'usd'
CHARGE_DESCRIPTION = 'Annual Premium Membership - 2024'
LIVE_MODE = False
```

## Example 4: European Pricing (EUR)

```python
# In charge_all_customers.py
CHARGE_AMOUNT_DOLLARS = 24.99  # €24.99
CURRENCY = 'eur'
CHARGE_DESCRIPTION = 'Monthly Subscription Fee'
LIVE_MODE = False
```

## Example 5: UK Pricing (GBP)

```python
# In charge_all_customers.py
CHARGE_AMOUNT_DOLLARS = 19.99  # £19.99
CURRENCY = 'gbp'
CHARGE_DESCRIPTION = 'Monthly Service Charge'
LIVE_MODE = False
```

## Common Amounts Reference

Just enter the dollar amount directly - super easy!

| Price    | In Code                          |
|----------|----------------------------------|
| $9.99    | `CHARGE_AMOUNT_DOLLARS = 9.99`   |
| $19.99   | `CHARGE_AMOUNT_DOLLARS = 19.99`  |
| $29.99   | `CHARGE_AMOUNT_DOLLARS = 29.99`  |
| $49.99   | `CHARGE_AMOUNT_DOLLARS = 49.99`  |
| $99.99   | `CHARGE_AMOUNT_DOLLARS = 99.99`  |
| $199.00  | `CHARGE_AMOUNT_DOLLARS = 199.00` |

## Running Schedule Examples

### Charge on 1st of Every Month
```bash
# Add to crontab (crontab -e)
0 9 1 * * cd /Users/aziz/Downloads/stripe-rebill && python3 charge_all_customers.py
```

### Charge Every Monday at 9 AM
```bash
0 9 * * 1 cd /Users/aziz/Downloads/stripe-rebill && python3 charge_all_customers.py
```

### Charge on 1st and 15th of Month
```bash
0 9 1,15 * * cd /Users/aziz/Downloads/stripe-rebill && python3 charge_all_customers.py
```

## Test Run Output Example

```
============================================================
STRIPE BATCH CHARGING SCRIPT
============================================================

Amount to charge: $29.99 USD
Description: Monthly Subscription Fee
Mode: 🟢 TEST MODE - Dry Run
Time: 2024-10-18 14:30:22

============================================================

⚠️  TEST MODE: No actual charges will be made
Set LIVE_MODE = True in the script to charge for real

📋 Retrieving customers from Stripe...

🔍 Checking payment methods...

✓ Found 25 customers with payment methods

============================================================
CUSTOMERS TO BE CHARGED:
============================================================
1. John Smith (john@example.com) - cus_ABC123
2. Jane Doe (jane@example.com) - cus_DEF456
3. Bob Johnson (bob@example.com) - cus_GHI789
...
25. Sarah Wilson (sarah@example.com) - cus_XYZ999

============================================================
Total charges: 25 customers × $29.99 = $749.75
============================================================

Press ENTER to continue with test run...

============================================================
CHARGING CUSTOMERS...
============================================================

[1/25] Charging John Smith (john@example.com)...
  ✓ TEST MODE: Would charge $29.99
[2/25] Charging Jane Doe (jane@example.com)...
  ✓ TEST MODE: Would charge $29.99
...

============================================================
RESULTS SUMMARY
============================================================

✓ Successful: 25 customers
✗ Failed: 0 customers

📄 Results saved to: charge_results_20241018_143045.txt

============================================================
COMPLETE!
============================================================
```

## Live Run Output Example

```
============================================================
STRIPE BATCH CHARGING SCRIPT
============================================================

Amount to charge: $29.99 USD
Description: Monthly Subscription Fee
Mode: 🔴 LIVE MODE - REAL CHARGES
Time: 2024-10-18 14:35:00

============================================================

[Shows customers list...]

⚠️  WARNING: You are about to charge REAL money!

Type 'YES' to proceed with charging: YES

============================================================
CHARGING CUSTOMERS...
============================================================

[1/25] Charging John Smith (john@example.com)...
  ✓ Success! Payment ID: pi_3AB4CD5EF6GH7IJ8
[2/25] Charging Jane Doe (jane@example.com)...
  ✓ Success! Payment ID: pi_3KL9MN0OP1QR2ST3
[3/25] Charging Bob Johnson (bob@example.com)...
  ✗ Card Error: Your card has insufficient funds.

...

============================================================
RESULTS SUMMARY
============================================================

✓ Successful: 23 customers
✗ Failed: 2 customers

💰 Total amount charged: $689.77 USD

============================================================
FAILED CHARGES:
============================================================

❌ Bob Johnson (bob@example.com)
   Customer ID: cus_GHI789
   Error: Your card has insufficient funds.

❌ Mike Davis (mike@example.com)
   Customer ID: cus_JKL012
   Error: Your card was declined.

📄 Results saved to: charge_results_20241018_143522.txt

============================================================
COMPLETE!
============================================================
```

