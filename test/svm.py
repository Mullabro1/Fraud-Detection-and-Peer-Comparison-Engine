import os
import json

# Define paths
script_directory = os.path.dirname(os.path.abspath(__file__))
json_folder = os.path.join(script_directory, "json")

balance_file = os.path.join(json_folder, "balance.json")
ratio_file = os.path.join(json_folder, "ratio.json")
calc_file = os.path.join(json_folder, "calc2.json")

def calc_cash_ratio(cash_equivalents, total_current_liabilities):
    """Calculate Cash Ratio: (Cash and Cash Equivalents) / Total Current Liabilities."""
    return cash_equivalents / total_current_liabilities if total_current_liabilities else 0

# Load balance data
with open(balance_file, "r") as f:
    balance_data = json.load(f)

# Load ratio data
with open(ratio_file, "r") as f:
    ratio_data = json.load(f)

# Prepare calculation results
calc_data = []
for balance_entry, ratio_entry in zip(balance_data, ratio_data):
    cash_ratio = calc_cash_ratio(
        balance_entry["cash_and_cash_equivalents"], 
        balance_entry["total_current_liabilities"]
    )
    
    calc_entry = {
        "org_id": balance_entry.get("org_id", 0),
        "type": balance_entry.get("type", "standalone"),
        "periods": [
            {
                "data_range": balance_entry["data_range"],
                "Cash_Ratio": cash_ratio,
                "Current_Ratio": ratio_entry.get("current_ratio", 0),
                "Quick_Ratio": ratio_entry.get("quick_ratio", 0)
            }
        ]
    }
    calc_data.append(calc_entry)

# Save the calculated results to calc.json
with open(calc_file, "w") as f:
    json.dump(calc_data, f, indent=4)

print("Cash Ratio, Current Ratio, and Quick Ratio calculations saved successfully in calc.json.")
