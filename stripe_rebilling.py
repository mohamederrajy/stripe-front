#!/usr/bin/env python3
"""
Stripe Subscription Rebilling Script
Handles recurring charges for subscription customers
"""

import stripe
import os
from datetime import datetime
from typing import List, Dict, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('stripe_rebilling.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class StripeRebilling:
    """Handle Stripe subscription rebilling operations"""
    
    def __init__(self, api_key: str):
        """
        Initialize Stripe rebilling handler
        
        Args:
            api_key: Your Stripe secret API key
        """
        stripe.api_key = api_key
        logger.info("Stripe API initialized")
    
    def create_subscription(self, customer_id: str, price_id: str) -> Dict:
        """
        Create a new subscription for a customer
        
        Args:
            customer_id: Stripe customer ID
            price_id: Stripe price ID for the subscription
            
        Returns:
            Dictionary containing subscription details
        """
        try:
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{'price': price_id}],
                payment_behavior='default_incomplete',
                expand=['latest_invoice.payment_intent']
            )
            logger.info(f"Subscription created for customer {customer_id}")
            return {
                'success': True,
                'subscription_id': subscription.id,
                'status': subscription.status,
                'subscription': subscription
            }
        except stripe.error.StripeError as e:
            logger.error(f"Error creating subscription: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def charge_customer(self, customer_id: str, amount: int, 
                       currency: str = 'usd', description: str = '') -> Dict:
        """
        Create a one-time charge for a customer
        
        Args:
            customer_id: Stripe customer ID
            amount: Amount in cents (e.g., 1000 = $10.00)
            currency: Currency code (default: 'usd')
            description: Charge description
            
        Returns:
            Dictionary containing charge details
        """
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                customer=customer_id,
                description=description,
                automatic_payment_methods={'enabled': True},
            )
            logger.info(f"Charge created for customer {customer_id}: ${amount/100:.2f}")
            return {
                'success': True,
                'payment_intent_id': payment_intent.id,
                'status': payment_intent.status,
                'amount': amount,
                'payment_intent': payment_intent
            }
        except stripe.error.StripeError as e:
            logger.error(f"Error charging customer: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def rebill_subscription(self, subscription_id: str) -> Dict:
        """
        Manually trigger a subscription billing cycle
        
        Args:
            subscription_id: Stripe subscription ID
            
        Returns:
            Dictionary containing billing result
        """
        try:
            # Create an invoice for the subscription
            invoice = stripe.Invoice.create(
                customer=subscription_id,
                subscription=subscription_id,
                auto_advance=True
            )
            
            # Finalize and pay the invoice
            invoice = stripe.Invoice.finalize_invoice(invoice.id)
            result = stripe.Invoice.pay(invoice.id)
            
            logger.info(f"Subscription {subscription_id} rebilled successfully")
            return {
                'success': True,
                'invoice_id': invoice.id,
                'status': result.status,
                'amount_paid': result.amount_paid,
                'invoice': result
            }
        except stripe.error.StripeError as e:
            logger.error(f"Error rebilling subscription: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def retry_failed_payment(self, invoice_id: str) -> Dict:
        """
        Retry a failed invoice payment
        
        Args:
            invoice_id: Stripe invoice ID
            
        Returns:
            Dictionary containing retry result
        """
        try:
            invoice = stripe.Invoice.pay(invoice_id)
            logger.info(f"Invoice {invoice_id} payment retry successful")
            return {
                'success': True,
                'invoice_id': invoice.id,
                'status': invoice.status,
                'amount_paid': invoice.amount_paid
            }
        except stripe.error.StripeError as e:
            logger.error(f"Error retrying payment: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_failed_invoices(self, limit: int = 100) -> List[Dict]:
        """
        Get list of failed invoices that need retry
        
        Args:
            limit: Maximum number of invoices to retrieve
            
        Returns:
            List of failed invoice dictionaries
        """
        try:
            invoices = stripe.Invoice.list(
                status='open',
                limit=limit
            )
            
            failed_invoices = []
            for invoice in invoices.auto_paging_iter():
                if invoice.attempted and not invoice.paid:
                    failed_invoices.append({
                        'invoice_id': invoice.id,
                        'customer_id': invoice.customer,
                        'amount': invoice.amount_due,
                        'attempt_count': invoice.attempt_count,
                        'created': datetime.fromtimestamp(invoice.created)
                    })
            
            logger.info(f"Found {len(failed_invoices)} failed invoices")
            return failed_invoices
        except stripe.error.StripeError as e:
            logger.error(f"Error retrieving failed invoices: {str(e)}")
            return []
    
    def get_all_customers(self, limit: int = 100) -> List[Dict]:
        """
        Get list of all customers in your Stripe account
        
        Args:
            limit: Maximum number of customers to retrieve
            
        Returns:
            List of customer dictionaries with ID, email, and payment methods
        """
        try:
            customers = stripe.Customer.list(limit=limit)
            
            customer_list = []
            for customer in customers.auto_paging_iter():
                # Get payment methods for this customer
                payment_methods = stripe.PaymentMethod.list(
                    customer=customer.id,
                    type='card'
                )
                
                has_payment_method = len(payment_methods.data) > 0
                
                customer_list.append({
                    'customer_id': customer.id,
                    'email': customer.email or 'No email',
                    'name': customer.name or 'No name',
                    'has_payment_method': has_payment_method,
                    'created': datetime.fromtimestamp(customer.created),
                    'description': customer.description or ''
                })
            
            logger.info(f"Found {len(customer_list)} customers")
            return customer_list
        except stripe.error.StripeError as e:
            logger.error(f"Error retrieving customers: {str(e)}")
            return []
    
    def get_active_subscriptions(self, limit: int = 100) -> List[Dict]:
        """
        Get list of all active subscriptions
        
        Args:
            limit: Maximum number of subscriptions to retrieve
            
        Returns:
            List of active subscription dictionaries
        """
        try:
            subscriptions = stripe.Subscription.list(
                status='active',
                limit=limit
            )
            
            active_subs = []
            for sub in subscriptions.auto_paging_iter():
                active_subs.append({
                    'subscription_id': sub.id,
                    'customer_id': sub.customer,
                    'status': sub.status,
                    'current_period_end': datetime.fromtimestamp(sub.current_period_end),
                    'amount': sub.items.data[0].price.unit_amount if sub.items.data else 0
                })
            
            logger.info(f"Found {len(active_subs)} active subscriptions")
            return active_subs
        except stripe.error.StripeError as e:
            logger.error(f"Error retrieving subscriptions: {str(e)}")
            return []
    
    def batch_rebill_customers(self, customer_ids: List[str], 
                               amount: int, currency: str = 'usd',
                               description: str = '') -> Dict:
        """
        Rebill multiple customers at once
        
        Args:
            customer_ids: List of Stripe customer IDs
            amount: Amount in cents to charge each customer
            currency: Currency code
            description: Charge description
            
        Returns:
            Dictionary with success/failure counts and details
        """
        results = {
            'successful': [],
            'failed': [],
            'total': len(customer_ids)
        }
        
        for customer_id in customer_ids:
            result = self.charge_customer(
                customer_id=customer_id,
                amount=amount,
                currency=currency,
                description=description
            )
            
            if result['success']:
                results['successful'].append({
                    'customer_id': customer_id,
                    'payment_intent_id': result['payment_intent_id'],
                    'amount': amount
                })
            else:
                results['failed'].append({
                    'customer_id': customer_id,
                    'error': result['error']
                })
        
        logger.info(f"Batch rebilling complete: {len(results['successful'])} successful, "
                   f"{len(results['failed'])} failed")
        return results
    
    def retry_all_failed_payments(self) -> Dict:
        """
        Retry all failed invoice payments
        
        Returns:
            Dictionary with retry results
        """
        failed_invoices = self.get_failed_invoices()
        results = {
            'successful': [],
            'failed': [],
            'total': len(failed_invoices)
        }
        
        for invoice in failed_invoices:
            result = self.retry_failed_payment(invoice['invoice_id'])
            
            if result['success']:
                results['successful'].append({
                    'invoice_id': invoice['invoice_id'],
                    'customer_id': invoice['customer_id'],
                    'amount': invoice['amount']
                })
            else:
                results['failed'].append({
                    'invoice_id': invoice['invoice_id'],
                    'customer_id': invoice['customer_id'],
                    'error': result['error']
                })
        
        logger.info(f"Failed payment retry complete: {len(results['successful'])} successful, "
                   f"{len(results['failed'])} failed")
        return results


def main():
    """Example usage of the Stripe rebilling script"""
    
    # Get API key from environment variable (RECOMMENDED) or set directly
    api_key = os.getenv('STRIPE_SECRET_KEY')
    
    if not api_key:
        print("ERROR: Please set STRIPE_SECRET_KEY environment variable")
        print("Example: export STRIPE_SECRET_KEY='sk_test_...'")
        return
    
    # Initialize the rebilling handler
    rebiller = StripeRebilling(api_key)
    
    print("\n=== Stripe Subscription Rebilling Script ===\n")
    print("Select an option:")
    print("1. View all customers (with payment methods)")
    print("2. Charge a single customer")
    print("3. Retry failed payments")
    print("4. View active subscriptions")
    print("5. View failed invoices")
    print("6. Batch rebill multiple customers")
    print("0. Exit")
    
    choice = input("\nEnter your choice: ").strip()
    
    if choice == '1':
        print("\nRetrieving all customers...")
        customers = rebiller.get_all_customers()
        
        print(f"\nFound {len(customers)} customers:\n")
        for cust in customers:
            print(f"Customer ID: {cust['customer_id']}")
            print(f"  Name: {cust['name']}")
            print(f"  Email: {cust['email']}")
            print(f"  Payment Method: {'✓ Yes' if cust['has_payment_method'] else '✗ No'}")
            if cust['description']:
                print(f"  Description: {cust['description']}")
            print(f"  Created: {cust['created']}")
            print()
    
    elif choice == '2':
        customer_id = input("Enter customer ID: ").strip()
        amount = int(input("Enter amount in cents (e.g., 1000 for $10.00): ").strip())
        description = input("Enter description: ").strip()
        
        result = rebiller.charge_customer(customer_id, amount, description=description)
        
        if result['success']:
            print(f"\n✓ Success! Payment Intent ID: {result['payment_intent_id']}")
            print(f"Status: {result['status']}")
            print(f"Amount: ${result['amount']/100:.2f}")
        else:
            print(f"\n✗ Error: {result['error']}")
    
    elif choice == '3':
        print("\nRetrying all failed payments...")
        results = rebiller.retry_all_failed_payments()
        
        print(f"\nTotal invoices: {results['total']}")
        print(f"Successful: {len(results['successful'])}")
        print(f"Failed: {len(results['failed'])}")
        
        if results['failed']:
            print("\nFailed retries:")
            for failed in results['failed']:
                print(f"  - Invoice {failed['invoice_id']}: {failed['error']}")
    
    elif choice == '4':
        print("\nRetrieving active subscriptions...")
        subscriptions = rebiller.get_active_subscriptions()
        
        print(f"\nFound {len(subscriptions)} active subscriptions:\n")
        for sub in subscriptions:
            print(f"Subscription ID: {sub['subscription_id']}")
            print(f"  Customer: {sub['customer_id']}")
            print(f"  Status: {sub['status']}")
            print(f"  Amount: ${sub['amount']/100:.2f}")
            print(f"  Next billing: {sub['current_period_end']}")
            print()
    
    elif choice == '5':
        print("\nRetrieving failed invoices...")
        invoices = rebiller.get_failed_invoices()
        
        print(f"\nFound {len(invoices)} failed invoices:\n")
        for inv in invoices:
            print(f"Invoice ID: {inv['invoice_id']}")
            print(f"  Customer: {inv['customer_id']}")
            print(f"  Amount: ${inv['amount']/100:.2f}")
            print(f"  Attempts: {inv['attempt_count']}")
            print(f"  Created: {inv['created']}")
            print()
    
    elif choice == '6':
        print("\nBatch rebilling customers")
        print("Enter customer IDs separated by commas:")
        customer_input = input().strip()
        customer_ids = [cid.strip() for cid in customer_input.split(',')]
        
        amount = int(input("Enter amount in cents (e.g., 1000 for $10.00): ").strip())
        description = input("Enter description: ").strip()
        
        print("\nProcessing batch rebilling...")
        results = rebiller.batch_rebill_customers(customer_ids, amount, description=description)
        
        print(f"\nTotal customers: {results['total']}")
        print(f"Successful: {len(results['successful'])}")
        print(f"Failed: {len(results['failed'])}")
        
        if results['failed']:
            print("\nFailed charges:")
            for failed in results['failed']:
                print(f"  - Customer {failed['customer_id']}: {failed['error']}")
    
    elif choice == '0':
        print("Exiting...")
        return
    
    else:
        print("Invalid choice")


if __name__ == '__main__':
    main()

