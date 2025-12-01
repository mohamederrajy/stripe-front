#!/bin/bash
#
# Simple script to charge all customers
# Just run: ./run_charging.sh
#

# Check if API key is set
if [ -z "$STRIPE_SECRET_KEY" ]; then
    echo "❌ ERROR: STRIPE_SECRET_KEY not set"
    echo ""
    echo "Please set your Stripe API key:"
    echo "  export STRIPE_SECRET_KEY='sk_test_your_key_here'"
    echo ""
    exit 1
fi

# Check if stripe is installed
if ! python3 -c "import stripe" 2>/dev/null; then
    echo "📦 Installing requirements..."
    pip3 install -r requirements.txt
fi

# Run the charging script
echo "🚀 Starting batch charging..."
python3 charge_all_customers.py

