# main.py
from datetime import datetime
from database.connection import client  # Ensures the connection is established
from models.transaction import Transaction
from models.statement import Statement
from models.card import Card

# # Create and save transactions
# transaction1 = Transaction(
#     transaction_date=datetime(2023, 5, 1),
#     clearing_date=datetime(2023, 5, 2),
#     description="Grocery shopping",
#     merchant="Supermarket",
#     category="Groceries",
#     type="debit",
#     amount_usd=150.75,
#     purchased_by="John Doe"
# )
# transaction1.save()

# transaction2 = Transaction(
#     transaction_date=datetime(2023, 5, 3),
#     clearing_date=datetime(2023, 5, 4),
#     description="Electronics purchase",
#     merchant="Electronics Store",
#     category="Electronics",
#     type="debit",
#     amount_usd=300.50,
#     purchased_by="John Doe"
# )
# transaction2.save()

# # Create and save a statement
# statement = Statement(
#     start_date=datetime(2023, 5, 1),
#     end_date=datetime(2023, 5, 31),
#     transactions=[transaction1, transaction2],
#     total_spending=0  # Initial value, will be calculated
# )
# statement.calculate_total_spending()  # Calculate total spending
# statement.save()

# Call the hardcode_cards method to insert the data
Card.hardcode_cards()

# Verify the data
cards = Card.objects()
for card in cards:
    print(f"Card Name: {card.name}, Cardholder Name: {card.cardholder_name}")
