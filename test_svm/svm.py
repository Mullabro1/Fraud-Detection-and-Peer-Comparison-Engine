import os
import json
import numpy as np
import pandas as pd
import shap
import matplotlib.pyplot as plt
import seaborn as sns
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import RobustScaler

# Get script directory
script_directory = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_directory, "output")
os.makedirs(output_dir, exist_ok=True)

def load_json_files(directory):
    """Loads all JSON files from a directory and extracts the 'data' key."""
    data = []
    full_path = os.path.join(script_directory, directory)
    if not os.path.exists(full_path):
        print(f"Warning: Directory {full_path} not found.")
        return []
    for file_name in os.listdir(full_path):
        if file_name.endswith(".json"):
            with open(os.path.join(full_path, file_name), 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                if isinstance(json_data, dict) and "data" in json_data:
                    data.extend(json_data["data"])
    return data

# Load training & testing data
train_data = load_json_files("train")
test_data = load_json_files("test")

if not train_data or not test_data:
    raise ValueError("Training or testing data is empty. Check the JSON files.")

train_df = pd.DataFrame(train_data)
test_df = pd.DataFrame(test_data)

# Extract company names
company_names = test_df.get("company_name", ["Unknown"] * len(test_df)).tolist()

# Drop irrelevant columns
drop_columns = ["sr.no", "company_name", "f.y._(fin._nature)", "product_/_service"]
train_df.drop(columns=drop_columns, inplace=True, errors='ignore')
test_df.drop(columns=drop_columns, inplace=True, errors='ignore')

# Convert all columns to numeric & handle missing values
train_df = train_df.apply(pd.to_numeric, errors='coerce')
test_df = test_df.apply(pd.to_numeric, errors='coerce')

# Fill NaN values with median (column-wise)
train_df.fillna(train_df.median(numeric_only=True), inplace=True)
test_df.fillna(test_df.median(numeric_only=True), inplace=True)

# Ensure target variable exists in test data
if "profit/(loss)" not in test_df.columns:
    test_df["profit/(loss)"] = 0  # Assign default zero

# Transform target variable
target_column = "profit_transformed"
train_df[target_column] = np.sign(train_df["profit/(loss)"]) * np.log1p(abs(train_df["profit/(loss)"]))
test_df[target_column] = np.sign(test_df["profit/(loss)"]) * np.log1p(abs(test_df["profit/(loss)"]))

# Feature Scaling (RobustScaler handles outliers well)
scaler = RobustScaler()
X_train = train_df.drop(columns=[target_column, "profit/(loss)"])
X_test = test_df.drop(columns=[target_column, "profit/(loss)"])

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

y_train = train_df[target_column]
y_test = test_df[target_column] if target_column in test_df else None

# Train XGBoost
xgb_model = XGBRegressor(
    objective="reg:squarederror",  # Standard regression objective
    n_estimators=50,               # Reduce to avoid overfitting on small data
    learning_rate=0.05,            # Lower LR for better generalization
    max_depth=3,                   # Restrict tree depth to prevent overfitting
    min_child_weight=2,            # Prevents overly small splits
    subsample=0.8,                 # Adds randomness to avoid overfitting
    colsample_bytree=0.8,          # Use only 80% of features per tree
    alpha=0.1,                      # L1 regularization (reduces feature reliance)
    reg_lambda=1.0,                 # L2 regularization (reduces overfitting)
    random_state=42                 # Ensure reproducibility
)

# Train model
xgb_model.fit(X_train_scaled, y_train)

# Make predictions
y_pred_xgb = xgb_model.predict(X_test_scaled)

# Evaluate Model
if y_test is not None and len(y_test) > 0:
    mae = mean_absolute_error(y_test, y_pred_xgb)
    r2 = r2_score(y_test, y_pred_xgb)

    print(f"XGBoost MAE: {mae:.4f}")  # More precise MAE
    print(f"XGBoost R² Score: {r2:.4f}")  # More precise R² score

    # Handle the case where R² is negative (indicating poor model performance)
    if r2 < 0:
        print("⚠️ Warning: The R² score is negative, indicating that the model is performing worse than a simple mean baseline.")

# Rank companies
ranked_companies = sorted(zip(company_names, y_pred_xgb), key=lambda x: x[1], reverse=True)
ranked_json = [{"rank": i+1, "company_name": name, "predicted_profit": float(pred)} for i, (name, pred) in enumerate(ranked_companies)]
with open(os.path.join(output_dir, "ranked_companies.json"), "w") as f:
    json.dump(ranked_json, f, indent=4)

# Generate ranked companies graph
plt.figure(figsize=(10, 6))
company_order = [x[0] for x in ranked_companies]
predicted_values = [x[1] for x in ranked_companies]
sns.barplot(y=company_order, x=predicted_values, palette="coolwarm")
plt.xlabel("Predicted Profit")
plt.ylabel("Company Name")
plt.title("Ranked Companies by Predicted Profit")
plt.savefig(os.path.join(output_dir, "ranked_companies_chart.png"), dpi=300, bbox_inches='tight')
plt.close()

# SHAP feature importance
try:
    explainer = shap.Explainer(xgb_model, X_train_scaled, feature_names=X_train.columns)
    shap_values = explainer(X_test_scaled)
    feature_names = list(X_train.columns)

    feature_contributions = {}
    top_loss_drivers = {}

    for i, company in enumerate(company_names):
        if i >= len(shap_values):
            continue

        company_shap = shap_values.values[i]
        sorted_indices = np.argsort(company_shap)
        ranked_features = [feature_names[idx] for idx in sorted_indices]
        ranked_shap_values = [float(company_shap[idx]) for idx in sorted_indices]

        feature_contributions[company] = {"features": ranked_features, "contributions": ranked_shap_values}

        if y_pred_xgb[i] < 0:
            top_loss_drivers[company] = {"features": ranked_features, "contributions": ranked_shap_values}

        plt.figure(figsize=(8, 4))
        sns.barplot(x=ranked_shap_values, y=ranked_features, palette="coolwarm")
        plt.xlabel("Feature Contribution")
        plt.ylabel("Feature")
        plt.title(f"{company} - Key Features Affecting Profit")
        plt.savefig(os.path.join(output_dir, f"{company}_feature_contributions.png"), dpi=300, bbox_inches='tight')
        plt.close()

    with open(os.path.join(output_dir, "feature_contributions.json"), "w") as f:
        json.dump(feature_contributions, f, indent=4)
    with open(os.path.join(output_dir, "top_loss_drivers.json"), "w") as f:
        json.dump(top_loss_drivers, f, indent=4)

    print("Feature contributions & top loss drivers JSONs saved.")

except Exception as e:
    print(f"SHAP analysis failed: {e}")
