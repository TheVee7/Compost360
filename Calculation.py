import joblib
import numpy as np

# Load the trained KNN model
knn_model = joblib.load('compost_gb_model.pkl')


# Example input data: [Day, Temperature, Moisture Content (%)]
input_data = np.array([[10, 28, 60]])  # Example: Day=10, Temp=28°C, Moisture=60%

# Make predictions
predictions = knn_model.predict(input_data)

# Print the predictions
print(f"Predicted Compost Maturity Score: {predictions[0][0]}")
print(f"Predicted Germination Index: {predictions[0][1]}")
