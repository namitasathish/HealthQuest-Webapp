from flask import Flask, request, jsonify
from model import predict_disease, get_disease_info
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Expects JSON data:
    {
      "symptoms": [
         {"symptom": "headache", "severity": 5},
         {"symptom": "fever", "severity": 8},
         ...
      ]
    }
    """
    data = request.get_json()
    if not data or 'symptoms' not in data:
        return jsonify({'error': 'Invalid input data. Provide a "symptoms" field.'}), 400

    user_symptoms = []
    for entry in data['symptoms']:
        try:
            symptom = entry['symptom']
            severity = float(entry['severity'])
            user_symptoms.append((symptom, severity))
        except (KeyError, ValueError):
            return jsonify({'error': 'Each symptom must have a valid "symptom" and numeric "severity" value.'}), 400

    top_predictions = predict_disease(user_symptoms, top_n=5)
    
    predictions_with_info = []
    for prediction in top_predictions:
        description, precautions = get_disease_info(prediction['disease'])
        predictions_with_info.append({
            'predicted_disease': prediction['disease'],
            'probability': prediction['probability'],
            'description': description,
            'precautions': precautions
        })
    
    return jsonify(predictions_with_info)

if __name__ == '__main__':
    app.run(debug=True)
