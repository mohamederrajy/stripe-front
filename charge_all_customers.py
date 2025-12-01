#!/usr/bin/env python3
"""
Simple Stripe Batch Charging Script
Charges all customers at once when you run it

IMPORTANT: Skips customers with Link, Google Pay, or Apple Pay
Only charges customers with regular card payment methods
"""

import stripe
import os
from datetime import datetime
import time

# ============================================
# CONFIGURATION - CHANGE THESE VALUES
# ============================================

# Amount to charge in DOLLARS (e.g., 29.99 for $29.99)
CHARGE_AMOUNT_DOLLARS = 1  # Change this to your subscription price

# Currency (usd, eur, gbp, etc.)
CURRENCY = 'usd'

# Description for the charge
CHARGE_DESCRIPTION = 'Monthly Subscription Fee'

# Set to True to actually charge, False to do a test run
LIVE_MODE = True  # Change to True when ready to charge for real

# STRIPE RADAR PROTECTION (Important!)
# Limit how many customers to charge (0 = no limit, all customers)
MAX_CUSTOMERS_TO_CHARGE = 1000  # Start with 10, increase after successful runs

# Delay between charges in seconds (helps avoid Stripe Radar blocks)
DELAY_BETWEEN_CHARGES = 0.1 # 1 second delay between each charge

# ============================================


def charge_all_customers():
    """Charge all customers with payment methods"""
    
    # Convert dollars to cents for Stripe API
    CHARGE_AMOUNT = int(CHARGE_AMOUNT_DOLLARS * 100)
    
    # Get API key from environment
    api_key = os.getenv('STRIPE_SECRET_KEY')
    if not api_key:
        print("ERROR: Please set STRIPE_SECRET_KEY environment variable")
        print("Example: export STRIPE_SECRET_KEY='sk_test_...'")
        return
    
    stripe.api_key = api_key
    
    print("\n" + "="*60)
    print("STRIPE BATCH CHARGING SCRIPT")
    print("="*60)
    print(f"\nAmount to charge: ${CHARGE_AMOUNT_DOLLARS:.2f} {CURRENCY.upper()}")
    print(f"Description: {CHARGE_DESCRIPTION}")
    print(f"Mode: {'🔴 LIVE MODE - REAL CHARGES' if LIVE_MODE else '🟢 TEST MODE - Dry Run'}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Show Stripe Radar protection settings
    if MAX_CUSTOMERS_TO_CHARGE > 0:
        print(f"\n🛡️  Radar Protection: Limiting to {MAX_CUSTOMERS_TO_CHARGE} customers")
    print(f"🛡️  Radar Protection: {DELAY_BETWEEN_CHARGES}s delay between charges")
    
    print("\n" + "="*60)
    
    if not LIVE_MODE:
        print("\n⚠️  TEST MODE: No actual charges will be made")
        print("Set LIVE_MODE = True in the script to charge for real\n")
    else:
        print("\n💡 TIP: Start with MAX_CUSTOMERS_TO_CHARGE = 10 for first run")
        print("   See STRIPE_RADAR_GUIDE.md for more info\n")
    
    # Get all customers
    print("\n📋 Retrieving customers from Stripe...")
    try:
        customers = stripe.Customer.list(limit=100)
    except Exception as e:
        print(f"❌ Error retrieving customers: {str(e)}")
        return
    
    # Filter customers with payment methods
    customers_to_charge = []
    skipped_count = 0
    print("\n🔍 Checking payment methods...")
    print("   (Skipping Link, Google Pay, Apple Pay)")
    
    for customer in customers.auto_paging_iter():
        # Check if customer has a VALID payment method (skip Link/Google Pay/Apple Pay)
        has_valid_card = False
        
        try:
            # Check all payment methods for this customer
            all_payment_methods = stripe.PaymentMethod.list(
                customer=customer.id,
                limit=10
            )
            
            # Look for regular card payment methods only
            for pm in all_payment_methods.data:
                # Skip Link, Google Pay, Apple Pay
                if pm.type in ['link', 'google_pay', 'apple_pay']:
                    continue
                
                # Only accept regular cards
                if pm.type == 'card':
                    # Additional check: make sure it's not a Link card
                    if hasattr(pm, 'link') and pm.link:
                        continue
                    has_valid_card = True
                    break
            
            # If no valid payment method found yet, check default_source (older API)
            if not has_valid_card and customer.default_source:
                # default_source is typically a regular card
                has_valid_card = True
            
            # If no valid payment method found yet, check invoice settings
            if not has_valid_card and customer.invoice_settings:
                if customer.invoice_settings.default_payment_method:
                    pm_id = customer.invoice_settings.default_payment_method
                    try:
                        pm = stripe.PaymentMethod.retrieve(pm_id)
                        if pm.type == 'card' and not (hasattr(pm, 'link') and pm.link):
                            has_valid_card = True
                    except:
                        pass
            
            if has_valid_card:
                customers_to_charge.append({
                    'id': customer.id,
                    'email': customer.email or 'No email',
                    'name': customer.name or 'No name'
                })
            else:
                skipped_count += 1
        except:
            continue
    
    print(f"\n✓ Found {len(customers_to_charge)} customers with regular card payment methods")
    if skipped_count > 0:
        print(f"⚠️  Skipped {skipped_count} customers (Link/Google Pay/Apple Pay)")
    
    if len(customers_to_charge) == 0:
        print("\n" + "="*60)
        print("⚠️  NO CUSTOMERS FOUND WITH REGULAR CARD PAYMENT METHODS")
        print("="*60)
        print("\nPossible reasons:")
        print("1. All customers have Link/Google Pay/Apple Pay (automatically skipped)")
        print("2. Using TEST key but have LIVE customers (or vice versa)")
        print("3. Customers paid but payment methods weren't saved")
        print("4. Using wrong Stripe account")
        print("\n💡 Run diagnostic to see details:")
        print("   python3 check_customers.py")
        print("\nOr check your Stripe Dashboard:")
        if stripe.api_key.startswith('sk_test'):
            print("   https://dashboard.stripe.com/test/customers")
        else:
            print("   https://dashboard.stripe.com/customers")
        print("="*60)
        return
    
    # Apply customer limit if set (helps avoid Stripe Radar blocks)
    if MAX_CUSTOMERS_TO_CHARGE > 0 and len(customers_to_charge) > MAX_CUSTOMERS_TO_CHARGE:
        print(f"\n⚠️  Limiting to {MAX_CUSTOMERS_TO_CHARGE} customers (MAX_CUSTOMERS_TO_CHARGE setting)")
        print(f"   Total customers available: {len(customers_to_charge)}")
        customers_to_charge = customers_to_charge[:MAX_CUSTOMERS_TO_CHARGE]
    
    # Show customers that will be charged
    print("\n" + "="*60)
    print("CUSTOMERS TO BE CHARGED:")
    print("="*60)
    for i, cust in enumerate(customers_to_charge, 1):
        print(f"{i}. {cust['name']} ({cust['email']}) - {cust['id']}")
    
    # Confirmation
    print("\n" + "="*60)
    total_amount = CHARGE_AMOUNT_DOLLARS * len(customers_to_charge)
    print(f"Total charges: {len(customers_to_charge)} customers × ${CHARGE_AMOUNT_DOLLARS:.2f} = ${total_amount:.2f}")
    print("="*60)
    
    if LIVE_MODE:
        print("\n⚠️  WARNING: You are about to charge REAL money!")
        confirm = input("\nType 'YES' to proceed with charging: ").strip()
        if confirm != 'YES':
            print("\n❌ Cancelled. No charges made.")
            return
    else:
        input("\nPress ENTER to continue with test run...")
    
    # Charge all customers
    print("\n" + "="*60)
    print("CHARGING CUSTOMERS...")
    print("="*60 + "\n")
    
    successful = []
    failed = []
    
    for i, customer in enumerate(customers_to_charge, 1):
        print(f"[{i}/{len(customers_to_charge)}] Charging {customer['name']} ({customer['email']})...")
        
        if not LIVE_MODE:
            # Test mode - simulate success
            print(f"  ✓ TEST MODE: Would charge ${CHARGE_AMOUNT_DOLLARS:.2f}")
            successful.append(customer)
            time.sleep(0.2)  # Small delay for readability
            continue
        
        # Live mode - actually charge
        try:
            # Get customer's default payment method
            cust_obj = stripe.Customer.retrieve(customer['id'])
            payment_method_id = None
            
            # Try to get payment method from invoice settings first
            if cust_obj.invoice_settings and cust_obj.invoice_settings.default_payment_method:
                payment_method_id = cust_obj.invoice_settings.default_payment_method
            # Otherwise try to get from payment methods list
            else:
                pms = stripe.PaymentMethod.list(customer=customer['id'], type='card', limit=1)
                if pms.data:
                    payment_method_id = pms.data[0].id
            
            if payment_method_id:
                # Charge using the specific payment method
                payment_intent = stripe.PaymentIntent.create(
                    amount=CHARGE_AMOUNT,
                    currency=CURRENCY,
                    customer=customer['id'],
                    payment_method=payment_method_id,
                    description=CHARGE_DESCRIPTION,
                    confirm=True,
                    off_session=True,
                    payment_method_types=['card'],
                )
            else:
                # Fallback: Try to charge with default source
                # This uses the older Sources API
                charge = stripe.Charge.create(
                    amount=CHARGE_AMOUNT,
                    currency=CURRENCY,
                    customer=customer['id'],
                    description=CHARGE_DESCRIPTION,
                )
                payment_intent = charge  # Use charge object for consistency
            
            print(f"  ✓ Success! Payment ID: {payment_intent.id}")
            successful.append(customer)
            
        except Exception as e:
            # Check if it's a card error (has user_message attribute)
            error_msg = getattr(e, 'user_message', str(e))
            print(f"  ✗ Error: {error_msg}")
            failed.append({'customer': customer, 'error': error_msg})
        
        # Delay between charges to avoid Stripe Radar blocks
        time.sleep(DELAY_BETWEEN_CHARGES)
    
    # Results summary
    print("\n" + "="*60)
    print("RESULTS SUMMARY")
    print("="*60)
    print(f"\n✓ Successful: {len(successful)} customers")
    print(f"✗ Failed: {len(failed)} customers")
    
    if LIVE_MODE:
        total_charged = len(successful) * CHARGE_AMOUNT_DOLLARS
        print(f"\n💰 Total amount charged: ${total_charged:.2f} {CURRENCY.upper()}")
    
    # Show failed charges
    if failed:
        print("\n" + "="*60)
        print("FAILED CHARGES:")
        print("="*60)
        for item in failed:
            cust = item['customer']
            error = item['error']
            print(f"\n❌ {cust['name']} ({cust['email']})")
            print(f"   Customer ID: {cust['id']}")
            print(f"   Error: {error}")
    
    # Save results to file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f"charge_results_{timestamp}.txt"
    
    with open(log_file, 'w') as f:
        f.write(f"Stripe Batch Charging Results\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Mode: {'LIVE' if LIVE_MODE else 'TEST'}\n")
        f.write(f"Amount: ${CHARGE_AMOUNT_DOLLARS:.2f} {CURRENCY.upper()}\n")
        f.write(f"\nSuccessful: {len(successful)}\n")
        f.write(f"Failed: {len(failed)}\n")
        
        if LIVE_MODE:
            f.write(f"\nTotal Charged: ${total_charged:.2f}\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write("SUCCESSFUL CHARGES:\n")
        f.write("="*60 + "\n")
        for cust in successful:
            f.write(f"{cust['name']} - {cust['email']} - {cust['id']}\n")
        
        if failed:
            f.write("\n" + "="*60 + "\n")
            f.write("FAILED CHARGES:\n")
            f.write("="*60 + "\n")
            for item in failed:
                cust = item['customer']
                f.write(f"{cust['name']} - {cust['email']} - {cust['id']}\n")
                f.write(f"  Error: {item['error']}\n\n")
    
    print(f"\n📄 Results saved to: {log_file}")
    print("\n" + "="*60)
    print("COMPLETE!")
    print("="*60 + "\n")


if __name__ == '__main__':
    charge_all_customers()

