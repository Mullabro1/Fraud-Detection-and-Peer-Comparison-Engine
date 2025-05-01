import json
import os
import statistics
#import spacy

# Define paths
script_directory = os.path.dirname(os.path.abspath(__file__))
output_directory = os.path.join(script_directory, "output")
os.makedirs(output_directory, exist_ok=True)
file_path = os.path.join(output_directory, "saved.json")
output_file = os.path.join(output_directory, "analysis.json")

def calculate_dynamic_thresholds(yoy_changes):
    """ Calculate mean and standard deviation for dynamic thresholds. """
    if len(yoy_changes) < 2:
        return 50, 100  # Default thresholds if not enough data
    
    mean = statistics.mean(yoy_changes)
    std_dev = statistics.stdev(yoy_changes)
    
    moderate_threshold = mean + std_dev  # 1σ above mean
    significant_threshold = mean + 2 * std_dev  # 2σ above mean
    
    return moderate_threshold, significant_threshold

def generate_nlg_summary(company_name, data_type, yoy_changes):
    """ Generate a natural language summary for ROE trends """
    if not yoy_changes:
        return f"YOY growth of ROE ({data_type}) has No data for analysis."

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
                    yoy_growth = data.get("yoy_growth", None)  # Default to None

                    if yoy_growth is None:
                        continue  # Skip missing data
                    
                    has_valid_data = True  # At least one valid entry exists
                    
                    # Capture YOY changes for summary
                    if i > 0:
                        yoy_changes.append((f"FY{years_sorted[i-1][-2:]}-{year[-2:]}", yoy_growth))
                
                if not has_valid_data:
                    return {
                        "yoy_growth_summary": generate_nlg_summary(name, data_type, []),
                        "analysis": ["No major fluctuations detected."]
                    }
                
                # Calculate dynamic thresholds
                yoy_values = [change[1] for change in yoy_changes]
                moderate_threshold, significant_threshold = calculate_dynamic_thresholds(yoy_values)
                
                for i, (year_range, yoy_growth) in enumerate(yoy_changes):
                    if abs(yoy_growth) >= significant_threshold:
                        analysis.append(f" Critical concern: ROE changed by {yoy_growth:.1f}% in {year_range}. Needs urgent review.")
                    elif abs(yoy_growth) >= moderate_threshold:
                        analysis.append(f" Significant variation: ROE fluctuated by {yoy_growth:.1f}% in {year_range}.")
                    elif abs(yoy_growth) >= 25:
                        analysis.append(f" Moderate concern: ROE fluctuated by {yoy_growth:.1f}% in {year_range}.")
                    
                    # Track consistent declines using a 3-year moving average
                    if i >= 2:  # At least 3 years of data needed
                        moving_avg = sum(yoy_values[i-2:i+1]) / 3
                        if moving_avg < 0:
                            analysis.append(" Consistent downward trend: ROE has declined over a 3-year period. Potential concern.")
                
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
