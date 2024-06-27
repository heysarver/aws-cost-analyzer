# /app/routes.py
from flask import Blueprint, render_template, request, jsonify
from .aws_utils import get_billing_data, get_linked_accounts

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    linked_accounts = get_linked_accounts()
    account_id = request.args.get('account_id')
    if account_id:
        billing_data = get_billing_data(account_id)
        return render_template('index.html', linked_accounts=linked_accounts, billing_data=billing_data, selected_account=account_id)
    return render_template('index.html', linked_accounts=linked_accounts)

@main.route('/api/billing_data', methods=['GET'])
def api_billing_data():
    account_id = request.args.get('account_id')
    if account_id:
        billing_data = get_billing_data(account_id)
        return jsonify(billing_data)
    else:
        return jsonify({"error": "No account selected"}), 400
