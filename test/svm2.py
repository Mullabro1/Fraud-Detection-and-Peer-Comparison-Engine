import os
import json
import csv

# Define paths
script_directory = os.path.dirname(os.path.abspath(__file__))
json_folder = os.path.join(script_directory, "json")

calc_file = os.path.join(json_folder, "calc.json")
insight_file = os.path.join(json_folder, "insight.json")

# Define CSV output files
csv_files = {
    "Cash_Ratio": os.path.join(json_folder, "cash_ratio.csv"),
    "Quick_Ratio": os.path.join(json_folder, "quick_ratio.csv"),
    "Current_Ratio": os.path.join(json_folder, "current_ratio.csv"),
}

# Thresholds for interpretation
TEMPLATES = {
    "Cash_Ratio": [
        (0.2, "🔴 *Critical liquidity risk: Cash Ratio is dangerously low (<0.2). The company might struggle to meet short-term obligations. Immediate action required.*", 
         "Critical liquidity risk: Cash Ratio is dangerously low (<0.2). The company might struggle to meet short-term obligations. Immediate action required."),
        (0.5, "⚠️ *Liquidity is tight (0.2 - 0.5). A low cash buffer may lead to financial stress. Consider increasing cash reserves.*", 
         "Liquidity is tight (0.2 - 0.5). A low cash buffer may lead to financial stress. Consider increasing cash reserves."),
        (1.0, "✅ *Optimal range (0.5 - 1.0). The company maintains strong liquidity while avoiding excess cash hoarding.*", 
         "Optimal range (0.5 - 1.0). The company maintains strong liquidity while avoiding excess cash hoarding."),
        (2.0, "⚠️ *Moderately high (1.0 - 2.0). While liquidity is strong, excess cash might not be efficiently deployed for growth.*", 
         "Moderately high (1.0 - 2.0). While liquidity is strong, excess cash might not be efficiently deployed for growth."),
        (float("inf"), "🔍 *Excessive cash reserves (>2.0). This could indicate underutilized funds. Strategic financial consulting recommended.*", 
         "Excessive cash reserves (>2.0). This could indicate underutilized funds. Strategic financial consulting recommended.")
    ],
    "Quick_Ratio": [
        (1.0, "🔴 *Warning: Quick Ratio is below 1.0. The company may struggle to meet short-term obligations without liquidating assets. Immediate review required.*", 
         "Warning: Quick Ratio is below 1.0. The company may struggle to meet short-term obligations without liquidating assets. Immediate review required."),
        (2.0, "✅ *Healthy range (1.0 - 2.0). The company has sufficient liquid assets to cover short-term liabilities efficiently.*", 
         "Healthy range (1.0 - 2.0). The company has sufficient liquid assets to cover short-term liabilities efficiently."),
        (3.0, "⚠️ *Caution: Quick Ratio is between 2.0 - 3.0. While liquidity is strong, excess assets may not be optimized for business growth.*", 
         "Caution: Quick Ratio is between 2.0 - 3.0. While liquidity is strong, excess assets may not be optimized for business growth."),
        (float("inf"), "🔍 *High Quick Ratio (>3.0) suggests potential inefficiencies in asset allocation. A financial review is recommended.*", 
         "High Quick Ratio (>3.0) suggests potential inefficiencies in asset allocation. A financial review is recommended.")
    ],
    "Current_Ratio": [
        (1.0, "🔴 *Urgent concern: Current Ratio below 1.0 signals potential difficulty in covering short-term liabilities. Immediate action needed.*", 
         "Urgent concern: Current Ratio below 1.0 signals potential difficulty in covering short-term liabilities. Immediate action needed."),
        (1.5, "⚠️ *Caution: Current Ratio is slightly low (1.0 - 1.5). Short-term liquidity may be stretched, requiring careful cash flow management.*", 
         "Caution: Current Ratio is slightly low (1.0 - 1.5). Short-term liquidity may be stretched, requiring careful cash flow management."),
        (3.0, "✅ *Optimal range (1.5 - 3.0). The company balances solvency and operational efficiency effectively.*", 
         "Optimal range (1.5 - 3.0). The company balances solvency and operational efficiency effectively."),
        (float("inf"), "🔍 *Current Ratio above 3.0 suggests underutilized assets that could be better invested for business growth.*", 
         "Current Ratio above 3.0 suggests underutilized assets that could be better invested for business growth.")
    ]
}

def analyze_ratio(name, value, json_format=True):
    """Determines interpretation based on ratio thresholds, keeping emojis for JSON and removing them for CSV."""
    for threshold, json_text, csv_text in TEMPLATES[name]:
        if value <= threshold:
            return json_text if json_format else csv_text
    return "🔍 *Ratio data missing. Further financial analysis required.*" if json_format else "Ratio data missing. Further financial analysis required."


# Load calc.json data
with open(calc_file, "r") as f:
    calc_data = json.load(f)

# Prepare CSV data structures
csv_data = {key: [] for key in csv_files.keys()}
insight_data = []

for entry in calc_data:
    org_id = entry["org_id"]
    org_type = entry["type"]
    periods = []
    
    for period in entry["periods"]:
        data_range = period["data_range"]
        period_insights = {"data_range": data_range}
        
        for ratio_name in ["Cash_Ratio", "Quick_Ratio", "Current_Ratio"]:
            ratio_value = period.get(ratio_name)
            ideal_range = "0.5-1.0" if ratio_name == "Cash_Ratio" else "1.0-2.0" if ratio_name == "Quick_Ratio" else "1.5-3.0"
            
            if ratio_value is not None:
                rounded_value = round(ratio_value, 2)
                interpretation_json = analyze_ratio(ratio_name, ratio_value, json_format=True)
                interpretation_csv = analyze_ratio(ratio_name, ratio_value, json_format=False)
                explanation = f"{ratio_name.replace('_', ' ')} is ideally within the range {ideal_range} for financial stability."
                
                period_insights[ratio_name.lower()] = [{
                    "ideal_range": ideal_range,
                    "explanation": explanation,
                    "company_range": f"{rounded_value}",
                    "interpretation": interpretation_json
                }]
                
                csv_data[ratio_name].append([
                    org_id, org_type, data_range, ideal_range, rounded_value, explanation, interpretation_csv
                ])
            else:
                period_insights[ratio_name.lower()] = [{
                    "ideal_range": "N/A",
                    "explanation": "Data missing.",
                    "company_range": "N/A",
                    "interpretation": "🔍 *Ratio data unavailable. Further analysis recommended.*"
                }]
                
                csv_data[ratio_name].append([
                    org_id, org_type, data_range, "N/A", "N/A", "Data missing.", "Ratio data unavailable. Further analysis recommended."
                ])
        
        periods.append(period_insights)
    
    insight_entry = {
        "org_id": org_id,
        "type": org_type,
        "periods": periods
    }
    insight_data.append(insight_entry)

# Save insights to insight.json
with open(insight_file, "w", encoding="utf-8") as f:
    json.dump(insight_data, f, indent=4, ensure_ascii=False)

# Write CSV files
for ratio_name, csv_path in csv_files.items():
    with open(csv_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(["org_id", "type", "data_range", "ideal_range", "company_value", "explanation", "interpretation"])
        writer.writerows(csv_data[ratio_name])

print("Financial insights saved successfully in insight.json and CSV files.")
