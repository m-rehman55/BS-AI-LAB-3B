from flask import Flask, render_template, request
import numpy as np
import pickle
import pandas as pd

# Flask Application initialize karna
app = Flask(__name__)

# Trained model ko load karna
model = None
try:
    with open('best_oil_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    print("Model loaded successfully.")
except FileNotFoundError:
    model = None
    print("ERROR: 'best_oil_model.pkl' file nahi mila. Kripya model save karein.")

@app.route('/')
def index():
    # Home page (index.html) ko render karna
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return render_template('index.html', prediction_text="Error: Model is not loaded.")

    try:
        features = []
        # Expected features count 6 hai (assuming Date, Open, High, Low, Vol., Change %)
        expected_features_count = 6 
        if hasattr(model, 'n_features_in_'):
            expected_features_count = model.n_features_in_
        
        # User se input lena
        for i in range(1, expected_features_count + 1): 
            feature_name = f'feature_{i}'
            # Data ko float mein convert karna
            features.append(float(request.form[feature_name]))

        # Input ko Numpy array mein convert karna
        final_features = np.array(features).reshape(1, -1)
        
        # Prediction
        prediction = model.predict(final_features)
        output = prediction[0]
        
        return render_template('index.html', prediction_text=f"Predicted Oil Value: {output}")

    except KeyError as e:
        return render_template('index.html', prediction_text=f"Input Error: Missing feature {e}. Expected {expected_features_count} features.")

    except Exception as e:
        return render_template('index.html', prediction_text=f"Processing Error: {e}. Check input values.")

if __name__ == '__main__':
    # Flask app ko run karna. Access: http://127.0.0.1:5000
    app.run(debug=True)