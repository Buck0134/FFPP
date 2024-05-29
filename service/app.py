import sys
import os
import pandas as pd
from datetime import datetime
from flask import Flask, request, jsonify, render_template
import traceback
# from financekit import create_financekit_blueprint

# Add the path to the `database` and `models` directories to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../database')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../models')))

from models.card import Card  # Import the Card model
from models.statement import Statement  # Import the Statement model
from models.transaction import Transaction  # Import the Transaction model
from database.connection import client  # Ensure the database connection is established

app = Flask(__name__)

# app.secret_key = 'your_secret_key'
# # Register the FinanceKit blueprint
# create_financekit_blueprint(app)

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


@app.route('/cards')
def data():
    return render_template('cards.html')


@app.route('/cards/<card_id>')
def card_statements(card_id):
    return render_template('statements.html')


@app.route('/statements/<statement_name>/transactions')
def statement_transactions(statement_name):
    return render_template('transactions.html')


@app.route('/hardcode_cards', methods=['GET'])
def hardcode_cards():
    Card.hardcode_cards()
    return jsonify({"message": "Cards hardcoded successfully"}), 200


@app.route('/cards/<card_name>/statements', methods=['GET'])
def get_statements_by_card(card_name):
    card = Card.objects(name=card_name).first()
    statements = [{"name": statement.name, "start_date": statement.start_date, "end_date": statement.end_date,
                   "total_spending": statement.calculate_total_spending()} for statement in Statement.objects(card=card)]
    return jsonify({"statements": statements})


@app.route('/cards/info', methods=['GET'])
def get_cards():
    cards = Card.objects()
    cards_list = []
    for card in cards:
        statements = Statement.objects(card=card)
        cards_list.append({"name": card.name, "cardholder_name": card.cardholder_name, "statements":
            [statement.name for statement in statements]})
    return jsonify(cards_list)


@app.route('/statements/<statement_name>/transactionsInfo', methods=['GET'])
def get_transactions_by_statement(statement_name):
    print(statement_name)
    statement = Statement.objects(name=statement_name).first()
    if not statement:
        return jsonify({"error": "Statement not found"}), 404

    transactions_data = [
        {
            'id': str(transaction.id),
            'date': transaction.transaction_date.strftime('%Y-%m-%d'),
            'description': transaction.description,
            'amount': float(transaction.amount_usd),
            'purchased_by':transaction.purchased_by
        }
        for transaction in statement.transactions
    ]
    print('Some')
    return jsonify({"transactions": transactions_data})


@app.route('/statements/<statement_name>', methods=['DELETE'])
def delete_statement(statement_name):
    try:
        statement = Statement.objects(name=statement_name).first()
        if not statement:
            return jsonify({"error": "Statement not found"}), 404

        # Delete all transactions associated with the statement
        Transaction.objects(statement=statement).delete()

        # Delete the statement itself
        statement.delete()

        return jsonify({"message": "Statement and its transactions deleted successfully"}), 200

    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/transactions/<transaction_id>/label', methods=['PUT'])
def label_transaction(transaction_id):
    data = request.get_json()
    purchased_by = data.get('purchased_by')

    if not purchased_by:
        return jsonify({"error": "Missing 'purchased_by' field"}), 400

    transaction = Transaction.objects(id=transaction_id).first()
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404

    transaction.purchased_by = purchased_by
    transaction.save()

    return jsonify({"message": "Transaction labeled successfully", "transaction": transaction.to_json()}), 200


def load_data(file_path):
    # Convert .xlsx to .csv if needed
    if file_path.endswith('.xlsx'):
        file_path = convert_xlsx_to_csv(file_path)

    # Extract card details from file name
    file_name = os.path.basename(file_path)
    card_name, date_str = file_name.replace('.csv', '').split('-', 1)

    # Find or create the card
    card = Card.objects(name=card_name).first()
    if not card:
        raise Exception("CARD NOT FOUND")
    # Read the CSV file
    data = pd.read_csv(file_path, encoding='ISO-8859-1')

    # Detect the statement format
    headers = data.columns
    if 'Extended Details' in headers:
        format_type = 1
    elif 'Clearing_Date' in headers:
        format_type = 2
    else:
        format_type = 3

    # Normalize data based on format
    transactions = []
    for _, row in data.iterrows():
        if format_type == 1:
            address = f"{row.get('Address', '')}, {row.get('City/State', '')}, {row.get('Zip Code', '')}, {row.get('Country', '')}"
            transaction = Transaction(
                transaction_date=datetime.strptime(str(row['Date']), '%m/%d/%Y'),
                description=str(row['Description']),
                amount_usd=float(row['Amount']),
                extended_details=str(row.get('Extended Details', '')),
                appears_on_statement_as=str(row.get('Appears On Your Statement As', '')),
                address=address,
                category=str(row.get('Category', '')),
                card=card
            )
        elif format_type == 2:
            transaction = Transaction(
                transaction_date=datetime.strptime(str(row['Transaction_Date']), '%m/%d/%Y'),
                clearing_date=datetime.strptime(str(row['Clearing_Date']), '%m/%d/%Y').date() if row['Clearing_Date'] else None,
                description=str(row['Description']),
                merchant=str(row.get('Merchant', '')),
                category=str(row['Category']),
                type=str(row.get('Type', '')),
                amount_usd=float(row['Amount (USD)']),
                purchased_by=str(row.get('Shared', '')),
                authorized_by=str(row.get('Purchased By', '')),
                card=card
            )
        else:  # format_type == 3
            transaction = Transaction(
                transaction_date=datetime.strptime(str(row['Date']), '%m/%d/%Y'),
                description=str(row['Description']),
                amount_usd=float(row['Amount']),
                merchant=str(row.get('Merchant', '')),
                category=str(row.get('Category', '')),
                card=card
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
        total_spending=0,  # Initial value, will be calculated
        name=card_name+'_'+date_str
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
            tb_str = traceback.format_exc()
            print(tb_str)
            return jsonify({"error": str(e), "traceback": tb_str}), 500
    else:
        return jsonify({"error": "Unsupported file type"}), 400


if __name__ == '__main__':
    app.run(debug=True)
