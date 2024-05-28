from datetime import datetime
from database.connection import client  # Ensures the connection is established
from models.transaction import Transaction
from models.statement import Statement
from models.card import Card

card = Card.objects(name="Amex_Gold").first()
# Insert new sample data
sample_data = [
    {
        "transaction_date": datetime(2023, 5, 27, 10, 0),
        "clearing_date": datetime(2023, 5, 28, 10, 0),
        "description": "Grocery Shopping",
        "merchant": "Supermarket",
        "category": "Groceries",
        "amount_usd": 150.75,
        "purchased_by": "John Doe",
        "statement": None,
        "card": card  # Replace with actual card reference if needed
    },
    {
        "transaction_date": datetime(2023, 5, 27, 11, 0),
        "clearing_date": None,
        "description": "Online Subscription",
        "merchant": "Streaming Service",
        "category": "Entertainment",
        "amount_usd": 9.99,
        "purchased_by": "Jane Doe",
        "statement": None,
        "card": card  # Replace with actual card reference if needed
    }
]

# Insert the sample data
for data in sample_data:
    transaction = Transaction(**data)
    transaction.save()

print("Transactions collection reinitialized with sample data.")