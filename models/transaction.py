import mongoengine as me

class Transaction(me.Document):
    transaction_date = me.DateTimeField(required=True)
    clearing_date = me.DateTimeField(required=True)
    description = me.StringField(required=True)
    merchant = me.StringField(required=True)
    category = me.StringField(required=True)
    type = me.StringField(required=True, choices=["debit", "credit"])
    amount_usd = me.DecimalField(required=True, precision=2)
    purchased_by = me.StringField(required=True)
    statement = me.ReferenceField('Statement', required=False)

    meta = {'collection': 'transactions'}