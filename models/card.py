import mongoengine as me
from models.statement import Statement

class Card(me.Document):
    name = me.StringField(required=True)
    card_number = me.StringField(required=True, unique=True)
    statements = me.ListField(me.ReferenceField(Statement), required=True)
    cardholder_name = me.StringField(required=True)

    meta = {'collection': 'cards'}

    def calculate_total_spending(self):
        return sum(statement.total_spending for statement in self.statements)

    @classmethod
    def hardcode_cards(cls):
        cards = [
            {"name": "Apple_Card", "card_number": "NULL", "cardholder_name": "Charlie Ji"},
            {"name": "Amex_Gold", "card_number": "NULL", "cardholder_name": "Bucky Yu"},
            {"name": "Amex_Plat", "card_number": "NULL", "cardholder_name": "Charlie Ji"},
            {"name": "BILT", "card_number": "NULL", "cardholder_name": "Bucky Yu"}
        ]
        
        for card_data in cards:
            card = cls(
                name=card_data["name"],
                card_number=card_data["card_number"],
                cardholder_name=card_data["cardholder_name"],
                statements=[]
            )
            card.save()
            print(f"Saved card: {card.name} for cardholder: {card.cardholder_name}")