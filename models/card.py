import mongoengine as me
from models.statement import Statement

class Card(me.Document):
    name = me.StringField(required=True)
    card_number = me.StringField(required=True, unique=True)
    statements = me.ListField(me.ReferenceField(Statement), required=False)
    cardholder_name = me.StringField(required=True)

    meta = {'collection': 'cards'}

    def calculate_total_spending(self):
        return sum(statement.total_spending for statement in self.statements)

    @classmethod
    def hardcode_cards(cls):
        cards = [
            {"name": "Apple_Card", "card_number": "5253636933895504", "cardholder_name": "Jiayi Ji"},
            {"name": "Amex_Gold", "card_number": "371698028922005", "cardholder_name": "Bucky Yu"},
            {"name": "Amex_Plat", "card_number": "371696128011000", "cardholder_name": "Jiayi Ji"},
            {"name": "BILT", "card_number": "5379861004135163", "cardholder_name": "Chenkai Yu"}
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

    @classmethod
    def delete_card(cls, card_name):
        if card_name == "ALL":
            # Fetch all cards
            cards = cls.objects.all()
        else:
            # Fetch the specific card
            cards = cls.objects(name=card_name)

        # Loop through each card and delete linked statements and transactions
        for card in cards:
            for statement in card.statements:
                for transaction in statement.transactions:
                    transaction.delete()
                statement.delete()
            card.delete()
            print(f"Deleted card: {card.name} and all linked statements and transactions")