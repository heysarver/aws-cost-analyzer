# /app/routes.py
from flask import Blueprint, render_template, request, jsonify
from .aws_utils import get_billing_data, get_linked_accounts

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    linked_accounts = get_linked_accounts()
    if request.method == 'POST':
        org_id = request.form.get('org_id')
        billing_data = get_billing_data(org_id)
        return render_template('report.html', billing_data=billing_data, linked_accounts=linked_accounts, selected_account=org_id)
    return render_template('index.html', linked_accounts=linked_accounts)

@main.route('/api/billing_data', methods=['POST'])
def api_billing_data():
    org_id = request.json.get('org_id')
    billing_data = get_billing_data(org_id)
    return jsonify(billing_data)
