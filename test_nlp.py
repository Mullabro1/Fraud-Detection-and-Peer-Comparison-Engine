import json
import os
import spacy

# Load spaCy model for natural language generation
nlp = spacy.blank("en")

# Define paths
script_directory = os.path.dirname(os.path.abspath(__file__))
output_directory = os.path.join(script_directory, "output")
os.makedirs(output_directory, exist_ok=True)
file_path = os.path.join(output_directory, "saved.json")
output_file = os.path.join(output_directory, "analysis.json")

def generate_nlg_summary(company_name, data_type, yoy_changes):
    """ Generate a natural language summary for ROE trends """
    if not yoy_changes:
        return f"YOY growth of ROE ({data_type}) is No data for analysis."

    summary = f"YOY growth of ROE ({data_type}) is "
    summary += ", ".join([f"{change:.1f}% in {year}" for year, change in yoy_changes]) + "."

    return summary

def analyze_roe_yoy():
    try:
        with open(file_path, "r") as file:
            companies = json.load(file)

        results = []

        for company in companies:
            name = company.get("organization_name", "Unknown")
            financials = company.get("financials", {})

            years_sorted = sorted(financials.keys())

            def analyze_type(data_type):
                analysis = []
                yoy_changes = []
                decline_streak = 0
                has_valid_data = False

                for i, year in enumerate(years_sorted):
                    data = financials[year].get(data_type, {})
                    yoy_growth = data.get("yoy_growth", 0)  # Default to 0 if None

                    if yoy_growth is None:
                        continue  # Skip missing data

                    has_valid_data = True  # At least one valid entry exists

                    # Capture YOY changes for summary
                    if i > 0:
                        yoy_changes.append((f"FY{years_sorted[i-1][-2:]}-{year[-2:]}", yoy_growth))

                    # Flag large variations
                    if abs(yoy_growth) >= 100:
                        analysis.append(f" Critical concern: ROE changed by {yoy_growth:.1f}% in {year}. Needs urgent review.")
                    elif abs(yoy_growth) >= 50:
                        analysis.append(f" Significant variation: ROE fluctuated by {yoy_growth:.1f}% in {year}.")
                    elif abs(yoy_growth) >= 25:
                        analysis.append(f" Moderate concern: ROE fluctuated by {yoy_growth:.1f}% in {year}.")

                    # Track consistent declines
                    if yoy_growth < 0:
                        decline_streak += 1
                    else:
                        decline_streak = 0

                    if decline_streak >= 3:
                        analysis.append(" Consistent downward trend: ROE has declined for 3+ consecutive years. Potential concern.")
                        decline_streak = 0  # Reset after flagging

                if not has_valid_data:
                    yoy_changes = []  # No valid data means no summary needed

                return {
                    "yoy_growth_summary": generate_nlg_summary(name, data_type, yoy_changes),
                    "analysis": analysis if analysis else ["No major fluctuations detected."]
                }

            standalone_result = analyze_type("standalone")
            consolidated_result = analyze_type("consolidated")

            results.append({
                "organization_name": name,
                "standalone": standalone_result,
                "consolidated": consolidated_result
            })

        with open(output_file, "w") as out:
            json.dump(results, out, indent=4)

        print("✅ Analysis saved in output/analysis.json")

    except Exception as e:
        print(f"❌ Error processing data: {e}")

analyze_roe_yoy()
