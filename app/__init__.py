from flask import Flask
from .routes import init_routes  # Import route initialization function

from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()



def create_app():
    app = Flask(__name__)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Initialize routes
    init_routes(app)
    
    return app