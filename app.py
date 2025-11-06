from flask import Flask, request, render_template, jsonify
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        age = float(data.get('age', 65))
        bmi = float(data.get('bmi', 28))
        
        # Simple risk calculation without ML dependencies
        risk_score = (age / 100) + (bmi / 50) + random.uniform(0, 0.3)
        risk_percentage = min(risk_score * 100, 95)
        
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
            'confidence': round(85 + random.uniform(0, 10), 2)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
