# /api/costs.py

import boto3
import datetime
from flask import jsonify, current_app
from . import api_bp

def sanitize_input(value):
    if isinstance(value, str):
        return value.replace(';', '').replace('--', '').replace('/*', '').replace('*/', '')
    return value

@api_bp.route('/costs/<org_id>/summary', methods=['GET'])
def get_cost_summary(org_id):
    input_org_id = sanitize_input(org_id)
    client = boto3.client('ce', 
                          aws_access_key_id=current_app.config.get('AWS_ACCESS_KEY_ID'), 
                          aws_secret_access_key=current_app.config.get('AWS_SECRET_ACCESS_KEY'))
    
    # Calculate date range for the last 3 months
    end_date = datetime.datetime.today().replace(day=1)
    start_date = (end_date - datetime.timedelta(days=1)).replace(day=1) - datetime.timedelta(days=60)
    end_date = end_date.strftime('%Y-%m-%d')
    start_date = start_date.strftime('%Y-%m-%d')
    
    try:
        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            Filter={
                'Dimensions': {
                    'Key': 'LINKED_ACCOUNT',
                    'Values': [input_org_id]
                }
            }
        )
        return jsonify(response['ResultsByTime'])
    except client.exceptions.ClientError as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/costs/<org_id>/by-service', methods=['GET'])
def get_cost_by_service(org_id):
    input_org_id = sanitize_input(org_id)
    client = boto3.client('ce', 
                          aws_access_key_id=current_app.config.get('AWS_ACCESS_KEY_ID'), 
                          aws_secret_access_key=current_app.config.get('AWS_SECRET_ACCESS_KEY'))
    
    # Calculate date range for the last 3 months
    end_date = datetime.datetime.today().replace(day=1)
    start_date = (end_date - datetime.timedelta(days=1)).replace(day=1) - datetime.timedelta(days=60)
    end_date = end_date.strftime('%Y-%m-%d')
    start_date = start_date.strftime('%Y-%m-%d')
    
    try:
        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[{
                'Type': 'DIMENSION',
                'Key': 'SERVICE'
            }],
            Filter={
                'Dimensions': {
                    'Key': 'LINKED_ACCOUNT',
                    'Values': [input_org_id]
                }
            }
        )
        return jsonify(response['ResultsByTime'])
    except client.exceptions.ClientError as e:
        return jsonify({'error': str(e)}), 500
