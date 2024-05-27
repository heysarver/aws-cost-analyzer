# /app.py
import os
from flask import Flask, render_template
from dotenv import load_dotenv
from config import load_config
from api import api_bp

load_dotenv()

app = Flask(__name__)
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('pages/index.html')

if __name__ == '__main__':
    config = load_config()
    app.run(host=config['FLASK_HOST'], port=config['FLASK_PORT'], debug=config['FLASK_DEBUG'])
