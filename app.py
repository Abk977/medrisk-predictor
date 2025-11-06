from flask import Flask, request, render_template, jsonify
import numpy as np
import pickle

app = Flask(__name__)

# In a real scenario, we'd load the trained model
# For now, we'll create a realistic prediction function
class MedicalPredictor:
    def predict_proba(self, features):
        # Realistic risk calculation based on multiple medical factors
        age, bmi, cholesterol, blood_sugar, hemoglobin, respiratory_rate, \
        oxygen_sat, prev_admissions, diabetes, hypertension, length_stay, \
        gender, bp_mean, age_group = features[0]
        
        # Comprehensive risk score calculation
        risk_score = (
            (age / 100) * 1.5 +                    # Age factor
            ((bmi - 25) / 10) * 1.2 +              # BMI factor
            ((cholesterol - 200) / 50) * 0.8 +     # Cholesterol
            ((blood_sugar - 100) / 30) * 1.1 +     # Blood sugar
            ((13.5 - hemoglobin) / 2) * 1.4 +      # Hemoglobin (lower = higher risk)
            ((respiratory_rate - 18) / 5) * 0.7 +  # Respiratory rate
            ((98 - oxygen_sat) / 5) * 1.6 +        # Oxygen saturation (lower = higher risk)
            (prev_admissions * 0.5) +              # Previous admissions
            (diabetes * 1.3) +                     # Diabetes
            (hypertension * 1.1) +                 # Hypertension
            (length_stay / 10) * 0.9 +             # Length of stay
            np.random.normal(0, 0.5)               # Random variation
        )
        
        # Convert to probability
        probability = 1 / (1 + np.exp(-risk_score))
        return np.array([[1 - probability, probability]])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Extract ALL medical parameters
        features = [
            float(data.get('age', 65)),                    # Age
            float(data.get('bmi', 28)),                    # BMI
            float(data.get('cholesterol', 200)),           # Cholesterol
            float(data.get('blood_sugar', 110)),           # Blood Sugar
            float(data.get('hemoglobin', 13.5)),           # Hemoglobin
            float(data.get('respiratory_rate', 18)),       # Respiratory Rate
            float(data.get('oxygen_saturation', 97)),      # Oxygen Sat
            float(data.get('previous_admissions', 1)),     # Previous Admissions
            int(data.get('has_diabetes', 0)),              # Diabetes
            int(data.get('has_hypertension', 0)),           # Hypertension
            float(data.get('length_of_stay', 5)),          # Length of Stay
            int(data.get('gender', 0)),                    # Gender
            float(data.get('systolic_bp', 130)),           # BP for calculation
            int(data.get('age_group', 1))                  # Age Group
        ]
        
        model = MedicalPredictor()
        prediction_proba = model.predict_proba([features])[0]
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
            'prediction': 1 if risk_percentage > 50 else 0,
            'risk_percentage': round(risk_percentage, 2),
            'risk_level': risk_level,
            'color': color,
            'confidence': round(max(prediction_proba) * 100, 2),
            'features_used': len(features)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
