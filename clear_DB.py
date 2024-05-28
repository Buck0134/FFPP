# main.py
from datetime import datetime
from database.connection import client  # Ensures the connection is established
from models.transaction import Transaction
from models.statement import Statement
from models.card import Card

Card.delete_card("ALL")
Statement.clear_statements()
Transaction.clear_transactions()


