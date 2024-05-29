import mongoengine as me
from payment import Payment
from mongoengine.queryset.visitor import Q

class Transaction(me.Document):
    transaction_date = me.DateTimeField(required=True)
    clearing_date = me.DateTimeField(required=False)
    description = me.StringField(required=True)
    merchant = me.StringField(required=False)
    category = me.StringField(required=True)
    amount_usd = me.DecimalField(required=True, precision=2)
    purchased_by = me.StringField(required=True, default="Unknown")
    authorized_by = me.StringField(required=False)
    extended_details = me.StringField(required=False)
    appears_on_statement_as = me.StringField(required=False)
    address = me.StringField(required=False)
    type = me.StringField(required=False)
    statement = me.ReferenceField('Statement', required=False)
    card = me.ReferenceField('Card', required=True)

    meta = {'collection': 'transactions'}

    @classmethod
    def clear_transactions(cls):
        cls.objects.delete()

    def parse_address(self):
        if self.address:
            parts = self.address.split(',')
            return {
                'address': parts[0] if len(parts) > 0 else '',
                'city_state': parts[1] if len(parts) > 1 else '',
                'zip_code': parts[2] if len(parts) > 2 else '',
                'country': parts[3] if len(parts) > 3 else ''
            }
    
    @classmethod
    def migrate_payments(cls):
        payment_descriptions = ["MOBILE PAYMENT", "PAYMENT", "DEPOSIT"]
        transactions = cls.objects(Q(description__icontains="MOBILE PAYMENT") |
                                   Q(description__icontains="PAYMENT") |
                                   Q(description__icontains="DEPOSIT"))
        for transaction in transactions:
            payment = Payment(
                transaction_date=transaction.transaction_date,
                clearing_date=transaction.clearing_date,
                description=transaction.description,
                merchant=transaction.merchant,
                category=transaction.category,
                amount_usd=transaction.amount_usd,
                purchased_by=transaction.purchased_by,
                authorized_by=transaction.authorized_by,
                extended_details=transaction.extended_details,
                appears_on_statement_as=transaction.appears_on_statement_as,
                address=transaction.address,
                type=transaction.type,
                statement=transaction.statement,
                card=transaction.card
            )
            payment.save()
            transaction.delete()
        
        print("Payment Transcations Migrated and Processed")
