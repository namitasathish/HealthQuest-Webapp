import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier

# -------------------------------------------
# 1. Load CSV Files: Training Data and Others
# -------------------------------------------

# Load the main dataset with diseases and their symptoms.
data = pd.read_csv("dataset.csv")
data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)
data.replace("", np.nan, inplace=True)

# Load the Symptom-severity mapping.
severity_df = pd.read_csv("Symptom-severity.csv")
severity_df = severity_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Create a dictionary mapping symptom (in lowercase) to its base weight.
severity_mapping = {}
for _, row in severity_df.iterrows():
    symptom = row["Symptom"].lower().strip()
    try:
        weight = float(row["weight"])
    except ValueError:
        weight = 1.0  # default if conversion fails
    severity_mapping[symptom] = weight

# Load disease descriptions.
desc_df = pd.read_csv("symptom_Description.csv")
desc_df = desc_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
description_dict = {}
for _, row in desc_df.iterrows():
    disease = row['Disease']
    description = row['Description']
    description_dict[disease] = description

# Load precaution recommendations.
precaution_df = pd.read_csv("symptom_precaution.csv")
precaution_df = precaution_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
precaution_dict = {}
for _, row in precaution_df.iterrows():
    disease = row['Disease']
    precautions = [row[col] for col in precaution_df.columns if col != 'Disease' and pd.notnull(row[col])]
    precaution_dict[disease] = precautions

# ---------------------------------------------------
# 2. Prepare the Training Data Using Weighted Features
# ---------------------------------------------------

# Identify the symptom columns (they start with "Symptom")
symptom_columns = [col for col in data.columns if col.lower().startswith("symptom")]

# Build a list of all unique symptoms found in the training dataset.
symptom_set = set()
for col in symptom_columns:
    symptoms_in_col = data[col].dropna().unique()
    for symptom in symptoms_in_col:
        symptom_set.add(symptom.strip())

# Fixed ordering of symptoms for feature vectors.
symptom_list = sorted(list(symptom_set))
print("List of all possible symptoms: ")
print(symptom_list)

# Function to create a feature vector for a training sample.
def create_feature_vector(row):
    features = [0] * len(symptom_list)
    for col in symptom_columns:
        symptom = row[col]
        if pd.isnull(symptom):
            continue
        symptom = symptom.strip()
        weight = severity_mapping.get(symptom.lower(), 1)
        try:
            idx = symptom_list.index(symptom)
            features[idx] = weight
        except ValueError:
            continue
    return features

# Build the feature matrix X and the target vector y.
X = data.apply(create_feature_vector, axis=1, result_type='expand')
y = data['Disease']

# ------------------------------------
# 3. Train a Simple Decision Tree Model
# ------------------------------------
model = DecisionTreeClassifier()
model.fit(X, y)

# -------------------------------------------------------
# 4. Prediction Function That Asks for Severity Inputs
# -------------------------------------------------------
def predict_disease(user_symptoms, top_n=5):
    """
    Given a list of (symptom, severity) pairs provided by the user,
    build a feature vector (weighted by base weights) and predict the top N diseases.
    """
    features = [0] * len(symptom_list)
    
    for symptom, user_severity in user_symptoms:
        symptom_clean = symptom.strip().lower()
        matched = False
        for i, s in enumerate(symptom_list):
            if s.lower() == symptom_clean:
                base_weight = severity_mapping.get(symptom_clean, 1)
                features[i] = user_severity * base_weight
                matched = True
                break
        if not matched:
            print(f"Warning: The symptom '{symptom}' was not recognized.")
    
    # Predict the probabilities for all diseases.
    probabilities = model.predict_proba([features])[0]
    
    # Get the indices of the top N predicted diseases based on the probabilities.
    top_indices = np.argsort(probabilities)[-top_n:][::-1]
    
    top_predictions = []
    for idx in top_indices:
        predicted_disease = model.classes_[idx]
        top_predictions.append({
            'disease': predicted_disease,
            'probability': probabilities[idx]
        })
    
    return top_predictions

# A helper function to get additional info for a predicted disease.
def get_disease_info(predicted_disease):
    description = description_dict.get(predicted_disease, "No description available.")
    precautions = precaution_dict.get(predicted_disease, ["No precautions available."])
    return description, precautions

if __name__ == '__main__':
    user_symptoms = [("headache", 5), ("fever", 8)]
    top_predictions = predict_disease(user_symptoms)
    for prediction in top_predictions:
        description, precautions = get_disease_info(prediction['disease'])
        print(f"Predicted Disease: {prediction['disease']}")
       
        print(f"Description: {description}")
        print(f"Precautions: {precautions}")
