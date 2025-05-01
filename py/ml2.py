import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

# Sample financial dataset (simulated)
data = {
    'Current_Ratio': [1.8, 0.9, 1.2, 2.1, 0.7, 1.5, 0.8, 1.3, 1.7, 0.7],
    'Debt_to_Equity': [0.8, 2.0, 1.4, 0.6, 2.5, 1.3, 2.1, 1.6, 0.9, 3.0],
    'OCF_to_Debt': [0.25, 0.10, 0.15, 0.30, 0.05, 0.18, 0.08, 0.12, 0.27, 0.03],
    'ROA': [0.08, 0.03, 0.05, 0.09, 0.01, 0.06, 0.02, 0.04, 0.07, -0.02],
    'Financial_Health': ['Healthy', 'Critical', 'At Risk', 'Healthy', 'Critical', 'At Risk', 'Critical', 'At Risk', 'Healthy', 'Critical']
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Define features and target
X = df.drop(columns=['Financial_Health'])
y = df['Financial_Health']

# Split dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train SVM Classifier
clf = SVC(kernel='linear', random_state=42)
clf.fit(X_train, y_train)

# Predict on test set
y_pred = clf.predict(X_test)

# Evaluate model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
