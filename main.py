# main.py
from datetime import datetime
from database.connection import client  # Ensures the connection is established
from models.transaction import Transaction
from models.statement import Statement
from models.card import Card

# Call the hardcode_cards method to insert the data
Card.hardcode_cards()

# Verify the data
cards = Card.objects()
for card in cards:
    print(f"Card Name: {card.name}, Cardholder Name: {card.cardholder_name}")
