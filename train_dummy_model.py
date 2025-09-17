import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

# Dummy training data: [download, upload, ping]
X = np.array([
    [100, 50, 10],
    [50, 20, 30],
    [10, 5, 100]
])
y = ["Excellent", "Good", "Poor"]

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save model
with open("backend/rf_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Dummy ML model saved as rf_model.pkl ✅")
