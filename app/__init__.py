from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    # Enable CORS
    CORS(app)
    
    # Get the absolute path to the models directory
    models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
    
    # Default configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        MODEL_PATH=os.path.join(models_dir, 'final_pycaret_model.pkl'),
        VECTORIZER_PATH=os.path.join(models_dir, 'tfidf_vectorizer.pkl'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.update(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register blueprints
    from .routes import main
    app.register_blueprint(main.bp)

    return app 