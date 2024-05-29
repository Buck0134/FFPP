from flask import Flask, redirect, url_for, session, request, Blueprint
from flask_oauthlib.client import OAuth
import requests

financekit_bp = Blueprint('financekit', __name__)
oauth = OAuth()

apple = oauth.remote_app(
    'apple',
    consumer_key='your_consumer_key',
    consumer_secret='your_consumer_secret',
    request_token_params={
        'scope': 'email',
    },
    base_url='https://api.apple.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://appleid.apple.com/auth/token',
    authorize_url='https://appleid.apple.com/auth/authorize'
)

@financekit_bp.route('/login')
def login():
    return apple.authorize(callback=url_for('financekit.authorized', _external=True))

@financekit_bp.route('/logout')
def logout():
    session.pop('apple_token')
    return redirect(url_for('financekit.index'))

@financekit_bp.route('/login/authorized')
def authorized():
    response = apple.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['apple_token'] = (response['access_token'], '')
    user_info = apple.get('userinfo')
    return 'Logged in as: ' + user_info.data['email']

@financekit_bp.route('/transactions')
def transactions():
    token = session.get('apple_token')[0]
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.get('https://api.apple.com/financekit/transactions', headers=headers)
    
    if response.status_code == 200:
        transactions = response.json()
        return transactions
    else:
        return f'Error fetching transactions: {response.status_code}'

@financekit_bp.route('/')
def index():
    return 'Welcome to the Apple FinanceKit integration example!'

@apple.tokengetter
def get_apple_oauth_token():
    return session.get('apple_token')

def create_financekit_blueprint(app):
    oauth.init_app(app)
    app.register_blueprint(financekit_bp, url_prefix='/financekit')
