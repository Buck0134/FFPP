import sys
import os
import pandas as pd
from datetime import datetime
from flask import Flask, request, jsonify, render_template

# Add the path to the `database` and `models` directories to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../database')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../models')))

from models.card import Card  # Import the Card model
from models.statement import Statement  # Import the Statement model
from models.transaction import Transaction  # Import the Transaction model
from database.connection import client  # Ensure the database connection is established


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_data():
    data = request.get_json()
    if data:
        card = Card(**data)
        card.save()
        return jsonify({"message": "Data added successfully"}), 201
    return jsonify({"message": "No data provided"}), 400

@app.route('/data', methods=['GET'])
def get_data():
    cards = Card.objects()
    cards_list = [{"name": card.name, "cardholder_name": card.cardholder_name} for card in cards]
    return jsonify(cards_list)

@app.route('/hardcode_cards', methods=['GET'])
def hardcode_cards():
    Card.hardcode_cards()
    return jsonify({"message": "Cards hardcoded successfully"}), 200

@app.route('/cards', methods=['GET'])
def get_cards():
    cards = Card.objects()
    cards_list = [{"name": card.name, "cardholder_name": card.cardholder_name} for card in cards]
    return jsonify(cards_list)

def load_data(file_path):
    # Convert .xlsx to .csv if needed
    if file_path.endswith('.xlsx'):
        file_path = convert_xlsx_to_csv(file_path)
    
    # Extract card details from file name
    file_name = os.path.basename(file_path)
    card_name, date_str = file_name.replace('.csv', '').split('-', 1)
    # Find or create the card
    card = Card.objects(name=card_name).first()
    # Read the CSV file
    data = pd.read_csv(file_path)
    
    # Create transactions
    transactions = []
    for _, row in data.iterrows():
        transaction = Transaction(
            transaction_date=datetime.strptime(row['Date'], '%m/%d/%Y'),
            description=row['Description'],
            amount_usd=row['Amount'],
            merchant=row.get('Merchant', ''),
            category=row.get('Category', ''),
            clearing_date=None,
            purchased_by=None,
            card=card  # Will be linked later
        )
        transaction.save()
        transactions.append(transaction)
    
    # Determine statement start and end dates
    statement_start_date = transactions[0].transaction_date
    statement_end_date = transactions[-1].transaction_date

    # Create and save a statement
    statement = Statement(
        start_date=statement_start_date,
        end_date=statement_end_date,
        transactions=transactions,
        total_spending=0  # Initial value, will be calculated
    )
    statement.calculate_total_spending()
    statement.save()
    
    # Link transactions to the statement
    for transaction in transactions:
        transaction.statement = statement
        transaction.save()
    
    card.statements.append(statement)
    
    card.save()
    
    # Link statement to the card
    statement.card = card
    statement.save()
    print(statement)
    return card.calculate_total_spending()

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and (file.filename.endswith('.csv') or file.filename.endswith('.xlsx')):
        file_path = os.path.join('/tmp', file.filename)
        file.save(file_path)
        
        try:
            total_spending = load_data(file_path)
            return jsonify({"message": "Data loaded successfully", "total_spending": total_spending}), 200
        except Exception as e:
            print(str(e))
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Unsupported file type"}), 400

if __name__ == '__main__':
    app.run(debug=True)