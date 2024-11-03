from .indexFiles import indexFiles_bp
from .query import query_bp
from .upload import upload_bp
from .purge import  purge_bp
from .chat import chat_bp
from .chat import end_chat_bp
from .listFiles  import list_files_bp

def init_routes(app):
    app.register_blueprint(indexFiles_bp)
    app.register_blueprint(query_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(purge_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(end_chat_bp)
    app.register_blueprint(list_files_bp)
