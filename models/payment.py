import mongoengine as me

class Payment(me.Document):
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

    meta = {'collection': 'payments'}