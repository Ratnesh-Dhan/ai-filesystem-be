from flask import Flask
from .routes import init_routes  # Import route initialization function

from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()



def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": os.getenv("FRONTEND", "*")}})
    
    # Initialize routes
    init_routes(app)
    
    return app