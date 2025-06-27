# HealthQuest Webapp

This project is a Health Symptom Checker that predicts the most likely disease based on symptoms and their severity using a Decision Tree Classifier. The system also provides a brief description of the condition and recommends precautionary measures, built with react as frontend 


## Features

- Predicts diseases based on user-input symptoms and severity scores.
- Provides disease descriptions for better understanding.
- Recommends precautionary steps to manage the condition.m.
- User-friendly and accessible via web browser.


## Working

1. User selects symptoms and rates their severity.
2. Symptoms are converted into a numerical vector using a base severity weight × user-input severity.
3. The feature vector is fed into a trained Decision Tree model.
4. The app displays:
   - Predicted Disease
   - Description of the disease
   - Suggested Precautions

## Dataset Files

- `dataset.csv` – Main training dataset mapping symptoms to diseases.
- `Symptom-severity.csv` – Maps each symptom to a severity weight.
- `symptom_Description.csv` – Short description of each disease.
- `symptom_precaution.csv` – List of precautionary steps for each disease.
