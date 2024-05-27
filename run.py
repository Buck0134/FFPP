from service.app import app
from models.card import Card  # Import the Card model
from database.connection import client  # Ensure the database connection is established

if __name__ == '__main__':
    Card.hardcode_cards()
    app.run(debug=True)
