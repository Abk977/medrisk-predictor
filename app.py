
import pickle
import numpy as np
from flask import Flask, request, render_template, jsonify
import os

app = Flask(__name__)

# For demo purposes - in real scenario we'd load trained models
class DemoModel:
    def predict_proba(self, X):
        # Simulate prediction probabilities
        return np.array([[0.7, 0.3]] if np.random.random() > 0.5 else [[0.2, 0.8]])
    def predict(self, X):
        return [1] if np.random.random() > 0.5 else [0]

# Use demo model for now
model = DemoModel()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Simulate prediction
        input_features = [float(data.get('age', 65)), float(data.get('bmi', 28))]
        prediction_proba = model.predict_proba([input_features])[0]
        prediction = model.predict([input_features])[0]
        
        risk_percentage = prediction_proba[1] * 100
        
        if risk_percentage < 20:
            risk_level = "Low Risk"
            color = "green"
        elif risk_percentage < 50:
            risk_level = "Medium Risk"
            color = "orange"
        else:
            risk_level = "High Risk"
            color = "red"
        
        return jsonify({
            'prediction': int(prediction),
            'risk_percentage': round(risk_percentage, 2),
            'risk_level': risk_level,
            'color': color,
            'confidence': round(max(prediction_proba) * 100, 2)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
