# /api/costs.py

import boto3
from flask import request, jsonify, current_app
from . import api_bp

def sanitize_input(value):
    if isinstance(value, str):
        return value.replace(';', '').replace('--', '').replace('/*', '').replace('*/', '')
    return value

@api_bp.route('/costs/<org_id>/summary', methods=['GET'])
def get_cost_summary(org_id):
    input_org_id = sanitize_input(org_id)
    client = boto3.client('ce', 
                          aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'], 
                          aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'])
    try:
        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': '2023-01-01', # Example period
                'End': '2023-01-31'
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
                          aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'], 
                          aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'])
    try:
        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': '2023-01-01',
                'End': '2023-01-31'
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
