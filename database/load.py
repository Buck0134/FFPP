import pandas as pd
from datetime import datetime
import os
from models.transaction import Transaction
from models.statement import Statement
from models.card import Card

def convert_xlsx_to_csv(xlsx_file_path):
    excel_data = pd.read_excel(xlsx_file_path, engine='openpyxl')
    csv_file_path = xlsx_file_path.replace('.xlsx', '.csv')
    excel_data.to_csv(csv_file_path, index=False)
    return csv_file_path

def load_data(file_path):
    # Convert .xlsx to .csv if needed
    if file_path.endswith('.xlsx'):
        file_path = convert_xlsx_to_csv(file_path)
    
    # Extract card details from file name
    file_name = os.path.basename(file_path)
    card_name, date_str = file_name.replace('.csv', '').split('_', 1)
    cardholder_name = "John Doe"  # This could be extracted or passed as a parameter if needed
    
    # Read the CSV file
    data = pd.read_csv(file_path)
    
    # Create transactions
    transactions = []
    for _, row in data.iterrows():
        transaction = Transaction(
            transaction_date=datetime.strptime(row['Date'], '%Y-%m-%d'),
            description=row['Description'],
            amount_usd=row['Amount'],
            merchant=row.get('Merchant', ''),
            category=row.get('Category', ''),
            clearing_date=None,
            purchased_by=None,
            card=None  # Will be linked later
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
    
    # Find or create the card
    card = Card.objects(name=card_name).first()
    if not card:
        card = Card(
            name=card_name,
            card_number="1234-5678-9876-5432",  # Example card number, adjust as necessary
            statements=[statement],
            cardholder_name=cardholder_name
        )
    else:
        card.statements.append(statement)
    
    card.save()
    
    # Link statement to the card
    statement.card = card
    statement.save()
    
    print(f"Data loaded successfully. Total Spending on {card.name}: {card.calculate_total_spending()}")
if __name__ == "__main__":
    load_data('path_to_your_file/Card_MM_DD_YY.csv')
