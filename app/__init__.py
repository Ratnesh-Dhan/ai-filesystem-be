from flask import Flask
from .routes import init_routes  # Import route initialization function

from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()



def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": os.getenv("FRONTEND", "*")}})
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,content-type,Temp-Session-ID')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    # Initialize routes
    init_routes(app)
    
    return app