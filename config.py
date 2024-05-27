# /config.py
import os
import argparse
from dotenv import load_dotenv

def load_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, help='Config file')
    args, unknown = parser.parse_known_args()

    if args.config:
        load_dotenv(args.config)
    else:
        load_dotenv()
    
    config = {
        'FLASK_HOST': os.environ.get('FLASK_HOST', '127.0.0.1'),
        'FLASK_PORT': int(os.environ.get('FLASK_PORT', 5000)),
        'FLASK_DEBUG': os.environ.get('FLASK_DEBUG', 'true').lower() == 'true',
        'AWS_ACCESS_KEY_ID': os.environ.get('AWS_ACCESS_KEY_ID'),
        'AWS_SECRET_ACCESS_KEY': os.environ.get('AWS_SECRET_ACCESS_KEY'),
        'AWS_ORG_ID': os.environ.get('AWS_ORG_ID')
    }
    return config
