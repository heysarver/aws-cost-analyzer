# /app/aws_utils.py
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

load_dotenv()

def get_aws_session():
    return boto3.Session(
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )

def get_linked_accounts():
    try:
        session = get_aws_session()
        org_client = session.client('organizations')
        
        accounts = [{'id': 'all', 'name': 'All Accounts (Combined)'}]  # Add the "All Accounts" option
        paginator = org_client.get_paginator('list_accounts')
        for page in paginator.paginate():
            for account in page['Accounts']:
                accounts.append({
                    'id': account['Id'],
                    'name': account['Name']
                })
        
        return accounts
    except ClientError as e:
        print(f"An error occurred while fetching linked accounts: {e}")
        return []

# /app/aws_utils.py

# ... (previous code remains the same)

def get_billing_data(account_id):
    try:
        session = get_aws_session()
        client = session.client('ce')
        
        org_id = os.getenv('AWS_ORG_ID')

        # Calculate date range
        end_date = datetime.now()
        start_date = (end_date.replace(day=1) - relativedelta(months=5)).replace(day=1)

        request = {
            'TimePeriod': {
                'Start': start_date.strftime('%Y-%m-%d'),
                'End': (end_date + timedelta(days=1)).strftime('%Y-%m-%d')  # Include today
            },
            'Granularity': 'MONTHLY',
            'Metrics': ['BlendedCost'],
            'GroupBy': [
                {'Type': 'DIMENSION', 'Key': 'SERVICE'},
            ]
        }

        if org_id and account_id and account_id != 'all':
            request['Filter'] = {
                'Dimensions': {
                    'Key': 'LINKED_ACCOUNT',
                    'Values': [account_id]
                }
            }
            request['GroupBy'].append({'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'})

        response = client.get_cost_and_usage(**request)
        
        # Process and sort the results
        processed_results = []
        for result in response['ResultsByTime']:
            month_start = datetime.strptime(result['TimePeriod']['Start'], '%Y-%m-%d')
            month_end = datetime.strptime(result['TimePeriod']['End'], '%Y-%m-%d') - timedelta(days=1)
            
            if month_end > end_date:
                month_end = end_date
            
            if start_date <= month_start <= end_date and result['Groups']:
                result['TimePeriod']['End'] = month_end.strftime('%Y-%m-%d')
                processed_results.append(result)

        sorted_results = sorted(processed_results, 
                                key=lambda x: datetime.strptime(x['TimePeriod']['Start'], '%Y-%m-%d'))
        
        return sorted_results
    except ClientError as e:
        print(f"An error occurred while fetching billing data: {e}")
        return None
