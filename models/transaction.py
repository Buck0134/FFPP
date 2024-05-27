import mongoengine as me

class Transaction(me.Document):
    transaction_date = me.DateTimeField(required=True)
    clearing_date = me.DateTimeField(required=False)
    description = me.StringField(required=True)
    merchant = me.StringField(required=False)
    category = me.StringField(required=True)
    amount_usd = me.DecimalField(required=True, precision=2)
    purchased_by = me.StringField(required=True, default="Unknown")
    statement = me.ReferenceField('Statement', required=False)
    card = me.ReferenceField('Card', required = True)

    meta = {'collection': 'transactions'}

    @classmethod
    def clear_transactions(cls):
        cls.objects.delete()