import React, { useState } from 'react';
import './App.css';

function App() {
  const [symptomEntries, setSymptomEntries] = useState([{ symptom: '', severity: '' }]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleEntryChange = (index, field, value) => {
    if (field === 'symptom') {
      // Allow only alphabetic characters and spaces
      const lettersOnly = /^[A-Za-z\s]*$/;
      if (!lettersOnly.test(value)) {
        return; // Do not update state if input contains invalid characters
      }
    }

    const newEntries = [...symptomEntries];
    newEntries[index][field] = value;
    setSymptomEntries(newEntries);
  };

  const addSymptomEntry = () => {
    setSymptomEntries([...symptomEntries, { symptom: '', severity: '' }]);
  };

  const removeSymptomEntry = (index) => {
    const newEntries = symptomEntries.filter((_, idx) => idx !== index);
    setSymptomEntries(newEntries);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const symptoms = symptomEntries.filter(
      entry => entry.symptom.trim() !== '' && entry.severity !== ''
    );
    const payload = { symptoms };

    try {
      const response = await fetch('http://localhost:5000/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
      setResult({ error: 'Failed to fetch prediction.' });
    }
    setLoading(false);
  };

  // Conditional class to move the form based on whether a result is shown or not
  const formClass = result ? 'move-to-top' : 'center-form';

  return (
    <div className="App">
      <header>
        <h1>HealthQuest Disease Prediction</h1>
      </header>
      <div className={`container ${formClass}`}>
        <form onSubmit={handleSubmit} className="symptom-form">
          {symptomEntries.map((entry, index) => (
            <div key={index} className="symptom-entry">
              <input
                type="text"
                placeholder="Enter symptom"
                value={entry.symptom}
                onChange={(e) => handleEntryChange(index, 'symptom', e.target.value)}
                required
              />
              <input
                type="number"
                placeholder="Severity (1-10)"
                min="1"
                max="10"
                value={entry.severity}
                onChange={(e) => handleEntryChange(index, 'severity', e.target.value)}
                required
              />
              <button type="button" onClick={() => removeSymptomEntry(index)} className="remove-btn">Remove</button>
            </div>
          ))}
          <button type="button" onClick={addSymptomEntry} className="add-btn">Add Symptom</button>
          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? 'Predicting...' : 'Predict'}
          </button>
        </form>

        {result && (
          <div className="result">
            {result.error ? (
              <p className="error">{result.error}</p>
            ) : (
              <>
                {result.map((prediction, index) => (
                  <div key={index} className="prediction-card">
                    <div className="prediction-content">
                      <h3>Predicted Disease: {prediction.predicted_disease}</h3>
                      <div className="prediction-details">
                        <p><strong>Description:</strong> {prediction.description}</p>
                        <div>
                          <strong>Precautions:</strong>
                          <ul>
                            {prediction.precautions.map((precaution, idx) => (
                              <li key={idx}>{precaution}</li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
