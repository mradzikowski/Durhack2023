import pandas as pd
import joblib

# Load the trained model and label encoder
model = joblib.load('model.pkl')
label_encoder = joblib.load('label_encoder.pkl')

# Load your test dataset (replace 'test_data.csv' with your test dataset filename)
test_data = pd.read_csv('test_set.csv')

# Feature selection: HomeTeam, AwayTeam
features = ['HomeTeam', 'AwayTeam']

# Use the label encoder to convert team names to numeric values
test_data['HomeTeam'] = label_encoder.transform(test_data['HomeTeam'])
test_data['AwayTeam'] = label_encoder.transform(test_data['AwayTeam'])

# Testing
X_test = test_data[features]

# Make predictions for Full-Time Result (FTR)
y_pred = model.predict(X_test)

# Map the numeric predictions back to result labels
result_labels = {0: 'H', 1: 'D', 2: 'A'}
y_pred_labels = [result_labels[pred] for pred in y_pred]

# Print the predicted Full-Time Results
print("Predicted Full-Time Results:")
print(y_pred_labels)
