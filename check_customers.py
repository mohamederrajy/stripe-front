#!/usr/bin/env python3
"""
Diagnostic script to check your Stripe customers
Shows why customers might not have payment methods
"""

import stripe
import os

# Get API key
api_key = os.getenv('STRIPE_SECRET_KEY')
if not api_key:
    print("ERROR: Please set STRIPE_SECRET_KEY")
    print("Run: export STRIPE_SECRET_KEY='sk_test_...'")
    exit(1)

stripe.api_key = api_key

print("\n" + "="*70)
print("STRIPE CUSTOMER DIAGNOSTIC")
print("="*70)

# Check which mode
if api_key.startswith('sk_test'):
    print("\n🧪 Using TEST MODE API key")
    print("   (You can only see TEST customers)")
elif api_key.startswith('sk_live'):
    print("\n🔴 Using LIVE MODE API key")
    print("   (You can only see LIVE/PRODUCTION customers)")
else:
    print("\n⚠️  Unknown API key format")

print("\n📋 Retrieving ALL customers from Stripe...")

try:
    customers = stripe.Customer.list(limit=100)
    customer_list = list(customers.auto_paging_iter())
    
    print(f"\n✓ Found {len(customer_list)} total customers in your account")
    
    if len(customer_list) == 0:
        print("\n❌ NO CUSTOMERS FOUND!")
        print("\nPossible reasons:")
        print("1. You're using a TEST key but have LIVE customers (or vice versa)")
        print("2. You don't have any customers in this Stripe account")
        print("\nCheck your Stripe Dashboard:")
        if api_key.startswith('sk_test'):
            print("   https://dashboard.stripe.com/test/customers")
        else:
            print("   https://dashboard.stripe.com/customers")
        exit(0)
    
    print("\n" + "="*70)
    print("CUSTOMER DETAILS:")
    print("="*70 + "\n")
    
    customers_with_pm = 0
    customers_with_source = 0
    customers_with_invoice_settings = 0
    
    for i, customer in enumerate(customer_list, 1):
        print(f"{i}. Customer ID: {customer.id}")
        print(f"   Email: {customer.email or 'No email'}")
        print(f"   Name: {customer.name or 'No name'}")
        print(f"   Created: {customer.created}")
        
        # Check for PaymentMethod (new way)
        payment_methods = stripe.PaymentMethod.list(
            customer=customer.id,
            type='card',
            limit=1
        )
        has_pm = len(payment_methods.data) > 0
        if has_pm:
            customers_with_pm += 1
            print(f"   ✅ Has PaymentMethod (card): YES")
        else:
            print(f"   ❌ Has PaymentMethod (card): NO")
        
        # Check for default source (old way)
        if customer.default_source:
            customers_with_source += 1
            print(f"   ✅ Has default source: YES ({customer.default_source})")
        else:
            print(f"   ❌ Has default source: NO")
        
        # Check invoice settings default payment method
        if customer.invoice_settings and customer.invoice_settings.default_payment_method:
            customers_with_invoice_settings += 1
            print(f"   ✅ Has invoice default PM: YES")
        else:
            print(f"   ❌ Has invoice default PM: NO")
        
        # Check for any sources
        if hasattr(customer, 'sources') and customer.sources.data:
            print(f"   📎 Has sources: {len(customer.sources.data)} source(s)")
        
        print()
    
    print("="*70)
    print("SUMMARY:")
    print("="*70)
    print(f"Total customers: {len(customer_list)}")
    print(f"Customers with PaymentMethod: {customers_with_pm}")
    print(f"Customers with default source: {customers_with_source}")
    print(f"Customers with invoice default PM: {customers_with_invoice_settings}")
    
    chargeable = max(customers_with_pm, customers_with_source, customers_with_invoice_settings)
    print(f"\n✅ Customers that CAN be charged: {chargeable}")
    
    if chargeable == 0:
        print("\n" + "="*70)
        print("⚠️  NO CUSTOMERS HAVE SAVED PAYMENT METHODS!")
        print("="*70)
        print("\nWhy this happens:")
        print("• Customers paid once but payment method wasn't saved")
        print("• You need to enable 'Save payment method' during checkout")
        print("• Or manually attach payment methods to customers")
        
        print("\n📖 Solutions:")
        print("\n1. For Future Payments - Enable saving payment methods:")
        print("   • Use Stripe Checkout with 'payment_method_collection'")
        print("   • Or use setup_future_usage='off_session' in Payment Intents")
        
        print("\n2. For Existing Customers - Use Stripe Billing:")
        print("   • Create Subscriptions instead of one-time charges")
        print("   • Stripe automatically saves payment methods for subscriptions")
        
        print("\n3. Ask customers to update their payment method:")
        print("   • Send them a Stripe hosted page to add a payment method")
        print("   • Use Stripe Customer Portal")
        
        print("\n4. Manually attach payment methods in Stripe Dashboard:")
        print("   • Go to each customer")
        print("   • Click 'Add payment method'")
        print("   • Enter their card details")
        
        print("\n" + "="*70)

except Exception as e:
    print(f"\n❌ Stripe Error: {str(e)}")
    print("\nThis might mean:")
    print("• Invalid API key")
    print("• API key doesn't have permission")
    print("• Network connection issue")

