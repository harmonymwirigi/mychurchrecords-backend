import stripe

# Set your Stripe test secret key
stripe.api_key = "sk_test_51OtZ2hDpVKhl93DHLGLN7FPuPSv5IfqG9AkkWFiosqVTI9cdbOzurfnv4TTXCKSNEzaBvZj7grXWEr9zeHPvlJpi00XA0mbCoc"

def create_charge_for_connected_account(amount, currency, connected_account_id):
    """
    Create a charge on a connected Stripe account.
    """
    try:
        # Create a charge for the connected account
        charge = stripe.Charge.create(
            amount=amount,  # Amount in cents (e.g., 500 cents = $5.00)
            currency=currency,
            source="tok_visa",  # Replace with a valid source or token
            description="Charge for connected account",
            capture=False,  # Set to False to authorize only
            stripe_account=connected_account_id  # Specify the connected account
        )
        print(f"Charge created successfully for {connected_account_id}: {charge.id}")
        return charge.id
    except Exception as e:
        print(f"Error creating charge: {e}")
        return None

def capture_charge_for_connected_account(charge_id, connected_account_id):
    """
    Capture a previously authorized charge for a connected account.
    """
    try:
        # Retrieve the charge for the connected account
        charge = stripe.Charge.retrieve(
            charge_id,
            stripe_account=connected_account_id  # Specify the connected account
        )
        # Capture the authorized charge
        charge.capture()
        print(f"Charge captured successfully for {connected_account_id}: {charge.id}")
    except Exception as e:
        print(f"Error capturing charge: {e}")

def main():
    # Account IDs
    platform_account_id = "acct_1OtZ2hDpVKhl93DH"  # Your main platform account
    connected_account_id = "acct_1PM9CnAntjgZRfuP"  # The connected account

    # Step 1: Create a charge of $5.00 (500 cents) with authorization only
    amount_in_cents = 500
    currency = "usd"
    
    charge_id = create_charge_for_connected_account(amount_in_cents, currency, connected_account_id)
    
    # Step 2: Capture the charge if it was successfully created
    if charge_id:
        capture_charge_for_connected_account(charge_id, connected_account_id)

if __name__ == "__main__":
    main()
