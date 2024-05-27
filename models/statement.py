# models/statement.py
import mongoengine as me
from models.transaction import Transaction

class Statement(me.Document):
    start_date = me.DateTimeField(required=True)
    end_date = me.DateTimeField(required=True)
    transactions = me.ListField(me.ReferenceField(Transaction), required=False)
    total_spending = me.DecimalField(required=True, precision=2)
    card = me.ReferenceField('Card', required=False)

    meta = {'collection': 'statements'}

    def calculate_total_spending(self):
        self.total_spending = sum(transaction.amount_usd for transaction in self.transactions)

    @classmethod
    def clear_statements(cls):
        cls.objects.delete()