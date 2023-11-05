import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt


# Load the dataset
data = pd.read_csv("combined_data.csv")

# Filter data for years 2000 to 2022
data = data[data['Date'].str[-2:] >= '00']
data = data[data['Date'].str[-2:] <= '22']

# Define input features and target variables
X = data[['HomeTeam', 'AwayTeam']]
y_FTHG = data['FTHG']
y_FTAG = data['FTAG']

# One-hot encode team names
encoder = OneHotEncoder(sparse=False)
X_encoded = encoder.fit_transform(X)

# Convert the encoded features into a DataFrame
X_encoded_df = pd.DataFrame(X_encoded, columns=encoder.get_feature_names_out(['HomeTeam', 'AwayTeam']))

# Combine the encoded features with the target variables
dataset_encoded = pd.concat([X_encoded_df, data[['FTHG', 'FTAG']]], axis=1)

# Train the model (Linear Regression is used as an example)
model_FTHG = LinearRegression()
model_FTHG.fit(X_encoded_df, y_FTHG)

model_FTAG = LinearRegression()
model_FTAG.fit(X_encoded_df, y_FTAG)

# Get user input for home and away teams
home_team = input("Enter the home team: ")
away_team = input("Enter the away team: ")

# Ensure the provided team names exist in the dataset
if home_team in X['HomeTeam'].values and away_team in X['AwayTeam'].values:
    # One-hot encode the input team names
    input_encoded = encoder.transform([[home_team, away_team]])

    predicted_FTHG = model_FTHG.predict(input_encoded)
    predicted_FTAG = model_FTAG.predict(input_encoded)

    print(f"Predicted FTHG: {predicted_FTHG[0]}")
    print(f"Predicted FTAG: {predicted_FTAG[0]}")
else:
    print("Team names not found in the dataset. Please provide valid team names.")


predicted_FTHG = model_FTHG.predict(X_encoded_df)
predicted_FTAG = model_FTAG.predict(X_encoded_df)

# Calculate the RMSE for FTHG and FTAG predictions
rmse_FTHG = np.sqrt(mean_squared_error(y_FTHG, predicted_FTHG))
rmse_FTAG = np.sqrt(mean_squared_error(y_FTAG, predicted_FTAG))

print(f"RMSE FTHG: {rmse_FTHG}")
print(f"RMSE FTAG: {rmse_FTAG}")
rmse_FTHG = 1.220663944196645
rmse_FTAG = 1.079071803385808

# Teams
teams = ['Home Game Wins', 'Away Game Wins']

# RMSE values for each team
rmse_values = [rmse_FTHG, rmse_FTAG]

# Create a bar chart
plt.bar(teams, rmse_values, color=['red', 'yellow'])
plt.xlabel('Team')
plt.ylabel('RMSE')
plt.title('Root Mean Squared Error (RMSE) for Goals Prediction')
plt.show()
