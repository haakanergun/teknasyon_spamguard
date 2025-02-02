from flask import Blueprint, render_template, jsonify, current_app
import random
import pandas as pd
import pickle
from pycaret.classification import load_model, predict_model
import os

bp = Blueprint('main', __name__)

# Load SMS dataset
def load_sms_dataset():
    try:
        df = pd.read_csv('datasets/sms_spam_train.csv')
        return df
    except Exception as e:
        current_app.logger.error(f"Error loading SMS dataset: {str(e)}")
        return None

# Global variables
_model = None
_vectorizer = None
_sms_dataset = None

def get_model():
    global _model
    if _model is None:
        model_path = current_app.config['MODEL_PATH']
        # Remove .pkl if it exists since PyCaret adds it automatically
        if model_path.endswith('.pkl'):
            model_path = model_path[:-4]
        current_app.logger.info(f"Loading model from: {model_path}")
        if not os.path.exists(model_path + '.pkl'):
            current_app.logger.error(f"Model file not found at: {model_path}.pkl")
            raise FileNotFoundError(f"Model file not found at: {model_path}.pkl")
        _model = load_model(model_path)
        current_app.logger.info("Model loaded successfully")
    return _model

def get_vectorizer():
    global _vectorizer
    if _vectorizer is None:
        vectorizer_path = current_app.config['VECTORIZER_PATH']
        current_app.logger.info(f"Loading vectorizer from: {vectorizer_path}")
        if not os.path.exists(vectorizer_path):
            current_app.logger.error(f"Vectorizer file not found at: {vectorizer_path}")
            raise FileNotFoundError(f"Vectorizer file not found at: {vectorizer_path}")
        with open(vectorizer_path, "rb") as f:
            _vectorizer = pickle.load(f)
        current_app.logger.info("Vectorizer loaded successfully")
    return _vectorizer

def get_sms_dataset():
    global _sms_dataset
    if _sms_dataset is None:
        _sms_dataset = load_sms_dataset()
    return _sms_dataset

def predict_sms(text: str) -> str:
    """
    Predict if an SMS is spam or ham.
    
    Args:
        text (str): The SMS message text
        
    Returns:
        str: 'spam' or 'ham'
    """
    try:
        # Preprocess text
        clean_text = text.lower()
        current_app.logger.info(f"Preprocessed text: {clean_text}")
        
        # Get model and vectorizer
        model = get_model()
        vectorizer = get_vectorizer()
        
        # Vectorize text
        text_vector = vectorizer.transform([clean_text])
        current_app.logger.info(f"Text vectorized. Shape: {text_vector.shape}")
        
        # Convert sparse matrix to dense array and create DataFrame
        features = pd.DataFrame(
            text_vector.toarray(),
            columns=vectorizer.get_feature_names_out()
        )
        current_app.logger.info(f"Created features DataFrame. Shape: {features.shape}")
        
        # Make prediction
        result = predict_model(model, data=features)
        current_app.logger.info(f"Prediction result columns: {result.columns.tolist()}")
        
        # Get the prediction column (it might be named 'prediction_label' or something similar)
        prediction_cols = [col for col in result.columns if 'prediction' in col.lower() or 'label' in col.lower()]
        if not prediction_cols:
            current_app.logger.error(f"No prediction column found. Available columns: {result.columns.tolist()}")
            raise ValueError("No prediction column found in model output")
            
        prediction_col = prediction_cols[0]
        current_app.logger.info(f"Using prediction column: {prediction_col}")
        
        # Get numerical prediction and convert to text label
        prediction = result.iloc[0][prediction_col]
        label = 'spam' if prediction == 1.0 else 'ham'
        
        current_app.logger.info(f"Successfully predicted message. Numerical prediction: {prediction}, Label: {label}")
        return label
    except Exception as e:
        current_app.logger.error(f"Error in predict_sms: {str(e)}")
        raise

@bp.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@bp.route('/get_message')
def get_message():
    """Get a random message and its classification."""
    try:
        # Get SMS dataset
        df = get_sms_dataset()
        if df is None:
            raise Exception("Failed to load SMS dataset")
        
        # Select random message
        random_row = df.iloc[random.randint(0, len(df)-1)]
        message = random_row['Message']
        label = random_row['Label'].lower()
        
        current_app.logger.info(f"Selected message: {message}")
        current_app.logger.info(f"Actual label: {label}")
        
        return jsonify({
            "status": "success",
            "message": message,
            "label": label
        })
    except Exception as e:
        current_app.logger.error(f"Error processing message: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "An error occurred while processing the message",
            "error": str(e)
        }), 500 