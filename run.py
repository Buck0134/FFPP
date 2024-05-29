from service.app import app
from models.card import Card  # Import the Card model
from models.transaction import Transaction
from database.connection import client  # Ensure the database connection is established

if __name__ == '__main__':
    Card.hardcode_cards()
    Transaction.migrate_payments()
    app.run(debug=True)
