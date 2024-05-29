# models/statement.py
import mongoengine as me
from models.transaction import Transaction
from bson import ObjectId
from bson.dbref import DBRef

class Statement(me.Document):
    start_date = me.DateTimeField(required=True)
    end_date = me.DateTimeField(required=True)
    transactions = me.ListField(me.ReferenceField(Transaction), required=False)
    total_spending = me.DecimalField(required=True, precision=2)
    card = me.ReferenceField('Card', required=False)
    name = me.StringField(required=True)

    meta = {'collection': 'statements'}

    def calculate_total_spending(self):
        self.remove_none_transactions()
        total_amount = 0
        for transcation in self.transactions:
            total_amount += transcation.amount_usd 
        self.total_spending = total_amount
        self.save()
        return self.total_spending

    @classmethod
    def clear_statements(cls):
        cls.objects.delete()
    
    def remove_none_transactions(self):
        valid_transactions = []
        for transaction in self.transactions:
            if transaction is None:
                continue

            if not isinstance(transaction, Transaction):
                continue
            
            valid_transactions.append(transaction)
        
        # Update the transactions list with valid transactions only
        self.transactions = valid_transactions
        self.save()