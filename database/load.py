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
    
    # Create and save transactions
    transactions = []
    for _, row in data.iterrows():
        transaction = Transaction(
            transaction_date=datetime.strptime(row['Transaction Date'], '%Y-%m-%d'),
            clearing_date=datetime.strptime(row['Clearing Date'], '%Y-%m-%d'),
            description=row['Description'],
            merchant=row['Merchant'],
            category=row['Category'],
            type=row['Type'].lower(),
            amount_usd=row['Amount (USD)'],
            purchased_by=row['Purchased By']
        )
        transaction.save()
        transactions.append(transaction)
    
    # Create and save a statement
    statement_start_date = datetime.strptime(date_str, '%m_%d_%y')
    statement_end_date = transactions[-1].transaction_date

    statement = Statement(
        start_date=statement_start_date,
        end_date=statement_end_date,
        transactions=transactions,
        total_spending=0  # Initial value, will be calculated
    )
    statement.calculate_total_spending()
    statement.save()
    
    # Create and save a card, or update if it already exists
    card = Card.objects(card_number="1234-5678-9876-5432").first()
    if not card:
        card = Card(
            name=card_name,
            card_number="1234-5678-9876-5432",
            statements=[statement],
            cardholder_name=cardholder_name
        )
    else:
        card.statements.append(statement)
    card.save()
    
    print(f"Data loaded successfully. Total Spending on {card.name}: {card.calculate_total_spending()}")

if __name__ == "__main__":
    load_data('path_to_your_file/Card_MM_DD_YY.csv')
