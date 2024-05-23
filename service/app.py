import sys
import os
from flask import Flask, request, jsonify, render_template

# Add the path to the `database` and `models` directories to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../database')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../models')))

from models.card import Card  # Import the Card model
from database.connection import client  # Ensure the database connection is established

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_data():
    data = request.get_json()
    if data:
        card = Card(**data)
        card.save()
        return jsonify({"message": "Data added successfully"}), 201
    return jsonify({"message": "No data provided"}), 400

@app.route('/data', methods=['GET'])
def get_data():
    cards = Card.objects()
    cards_list = [{"name": card.name, "cardholder_name": card.cardholder_name} for card in cards]
    return jsonify(cards_list)

@app.route('/hardcode_cards', methods=['GET'])
def hardcode_cards():
    Card.hardcode_cards()
    return jsonify({"message": "Cards hardcoded successfully"}), 200

@app.route('/cards', methods=['GET'])
def get_cards():
    cards = Card.objects()
    cards_list = [{"name": card.name, "cardholder_name": card.cardholder_name} for card in cards]
    return jsonify(cards_list)