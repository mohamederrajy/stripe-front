# Stripe Subscription Rebilling Script

A Python script for managing Stripe subscription billing, rebilling customers, and handling failed payments.

## Features

- ✅ Charge individual customers for subscription renewals
- ✅ Batch rebill multiple customers at once
- ✅ Retry failed payments automatically
- ✅ View active subscriptions
- ✅ Track failed invoices
- ✅ Comprehensive logging
- ✅ Error handling and reporting

## Prerequisites

- Python 3.7 or higher
- A Stripe account with API keys
- Active customer payment methods in Stripe

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your Stripe API key:**

   **Option A: Environment Variable (Recommended)**
   ```bash
   export STRIPE_SECRET_KEY='sk_test_your_key_here'
   ```

   **Option B: .env file**
   ```bash
   cp .env.example .env
   # Edit .env and add your Stripe secret key
   ```

3. **Get your Stripe API keys:**
   - Go to https://dashboard.stripe.com/apikeys
   - Use **test keys** (sk_test_...) for testing
   - Use **live keys** (sk_live_...) for production

## Usage

### Interactive Mode

Run the script with the interactive menu:

```bash
python stripe_rebilling.py
```

You'll see options to:
1. Charge a single customer
2. Retry failed payments
3. View active subscriptions
4. View failed invoices
5. Batch rebill multiple customers

### Programmatic Usage

Use the script in your own Python code:

```python
from stripe_rebilling import StripeRebilling

# Initialize
rebiller = StripeRebilling('sk_test_your_key_here')

# Charge a single customer
result = rebiller.charge_customer(
    customer_id='cus_xxxxxxxxxxxxx',
    amount=2999,  # $29.99 in cents
    description='Monthly subscription - January 2024'
)

# Retry all failed payments
results = rebiller.retry_all_failed_payments()

# Batch rebill multiple customers
customer_ids = ['cus_111', 'cus_222', 'cus_333']
results = rebiller.batch_rebill_customers(
    customer_ids=customer_ids,
    amount=1999,  # $19.99
    description='Subscription renewal'
)

# Get active subscriptions
subscriptions = rebiller.get_active_subscriptions()

# Get failed invoices
failed = rebiller.get_failed_invoices()
```

## Examples

### Example 1: Charge a Single Customer

```python
rebiller = StripeRebilling(api_key)

result = rebiller.charge_customer(
    customer_id='cus_xxxxxxxxxxxxx',
    amount=4999,  # $49.99
    currency='usd',
    description='Premium subscription - Month 1'
)

if result['success']:
    print(f"Charged successfully! Payment ID: {result['payment_intent_id']}")
else:
    print(f"Error: {result['error']}")
```

### Example 2: Retry Failed Payments

```python
rebiller = StripeRebilling(api_key)

# Get all failed invoices
failed_invoices = rebiller.get_failed_invoices()

# Retry each one
for invoice in failed_invoices:
    result = rebiller.retry_failed_payment(invoice['invoice_id'])
    if result['success']:
        print(f"Invoice {invoice['invoice_id']} paid successfully")
```

### Example 3: Batch Rebilling

```python
rebiller = StripeRebilling(api_key)

# List of customers to rebill
customers = ['cus_AAA', 'cus_BBB', 'cus_CCC']

# Rebill all at once
results = rebiller.batch_rebill_customers(
    customer_ids=customers,
    amount=2999,  # $29.99
    description='Monthly subscription renewal'
)

print(f"Successful: {len(results['successful'])}")
print(f"Failed: {len(results['failed'])}")
```

## Important Notes

### Test Mode vs Live Mode

- **Always test with test keys first** (sk_test_...)
- Test mode won't charge real cards
- Use Stripe's test card numbers: https://stripe.com/docs/testing

### Customer Consent

- Ensure customers have agreed to recurring charges
- Include clear terms in your subscription agreement
- Follow Stripe's best practices for subscriptions

### Error Handling

The script handles common errors:
- Invalid customer IDs
- Declined cards
- Insufficient funds
- Network issues
- API errors

All operations are logged to `stripe_rebilling.log`

### Best Practices

1. **Start with test mode** - Use test API keys initially
2. **Check customer status** - Verify customers exist before charging
3. **Handle failures gracefully** - Not all charges will succeed
4. **Log everything** - Review logs regularly
5. **Set up webhooks** - Use Stripe webhooks for real-time notifications
6. **Comply with regulations** - Follow payment processing laws in your region

## Logging

All operations are logged to `stripe_rebilling.log` with timestamps:

```
2024-01-15 10:30:45 - INFO - Stripe API initialized
2024-01-15 10:31:02 - INFO - Charge created for customer cus_xxx: $29.99
2024-01-15 10:31:15 - ERROR - Error charging customer: Card was declined
```

## Security

- **Never commit your API keys** to version control
- Use environment variables for API keys
- Restrict API key permissions in Stripe Dashboard
- Use test keys for development
- Rotate keys regularly

## Troubleshooting

### "No such customer" error
- Verify the customer ID exists in your Stripe account
- Check you're using the correct API key (test vs live)

### "Card declined" error
- Customer's payment method may have expired
- Insufficient funds
- Card issuer declined the charge
- Use `retry_failed_payment()` after customer updates their card

### "Invalid API key" error
- Check your STRIPE_SECRET_KEY is set correctly
- Ensure the key starts with `sk_test_` or `sk_live_`
- Verify the key hasn't been rolled/deleted in Stripe Dashboard

## Support

- Stripe Documentation: https://stripe.com/docs
- Stripe API Reference: https://stripe.com/docs/api
- Stripe Support: https://support.stripe.com

## License

This script is provided as-is for educational and commercial use.

