from flask import Flask
from flask_cors import CORS
from app.utils.image_analysis import configure_palm

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS
    
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.config['PALM_API_KEY'] = 'YOUR_API_KEY_HERE'  # Make sure this is set

    # Configure PaLM
    configure_palm(app.config['PALM_API_KEY'])

    # Register routes
    from app.routes import main
    app.register_blueprint(main)

    return app 