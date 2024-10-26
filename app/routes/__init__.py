from .indexFiles import indexFiles_bp
from .query import query_bp
from .upload import upload_bp

def init_routes(app):
    app.register_blueprint(indexFiles_bp)
    app.register_blueprint(query_bp)
    app.register_blueprint(upload_bp)