# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.preprocessing import LabelEncoder
# import joblib
#
# # Load your historical match data from the provided CSV file
# # Load your historical match data from the provided CSV file
# data = pd.read_csv('combined_data.csv', encoding='utf-8', low_memory=False)
#
#
# # Feature selection: HomeTeam, AwayTeam
# features = ['HomeTeam', 'AwayTeam']
# target = 'FTR'  # Full-Time Result (H=Home Win, D=Draw, A=Away Win)
#
# # Check if the columns 'HomeTeam' and 'AwayTeam' are present in the dataset
# if 'HomeTeam' not in data.columns or 'AwayTeam' not in data.columns:
#     raise KeyError("The columns 'HomeTeam' and 'AwayTeam' are not found in the dataset. Please verify the column names in the CSV file.")
#
# # Use LabelEncoder to convert team names to numeric values
# label_encoder = LabelEncoder()
# data['HomeTeam'] = label_encoder.fit_transform(data['HomeTeam'])
# data['AwayTeam'] = label_encoder.transform(data['AwayTeam'])
# #
# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(data[features], data[target], test_size=0.2, random_state=42)
#
# # Train a classification model
# model = RandomForestClassifier(n_estimators=100, random_state=42)
# model.fit(X_train, y_train)
#
# # Save the trained model and label encoder
# joblib.dump(model, 'model.pkl')
# joblib.dump(label_encoder, 'label_encoder.pkl')
