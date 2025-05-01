import json
import os

# Define the path to the input and output JSON files
script_directory = os.path.dirname(os.path.abspath(__file__))
input_directory = os.path.join(script_directory, "input")
output_directory = os.path.join(script_directory, "output")

input_file_path = os.path.join(input_directory, "saved.json")
output_file_path = os.path.join(output_directory, "saved.json")

def calculate_roe_yoy():
    try:
        # Read JSON file
        with open(input_file_path, "r") as file:
            companies = json.load(file)

        results = []

        for company in companies:
            name = company.get("organization_name", "Unknown")
            financials = company.get("financials", {})

            company_result = {"organization_name": name, "financials": {}}
            roe_history = {"standalone": {}, "consolidated": {}}
            years_sorted = sorted(financials.keys())  # Sort years

            for year in years_sorted:
                company_result["financials"][year] = {}

                # Process Standalone
                if "standalone" in financials[year]:
                    data = financials[year]["standalone"]
                    try:
                        profit_loss = float(data.get("profit_loss", "N/A"))
                        networth = float(data.get("networth", "N/A"))

                        if networth != 0:
                            roe = (profit_loss / networth) * 100
                        else:
                            roe = None  # Avoid division by zero

                    except ValueError:
                        roe = None  # Invalid data

                    company_result["financials"][year]["standalone"] = {
                        "profit_loss": data.get("profit_loss", "N/A"),
                        "networth": data.get("networth", "N/A"),
                        "roe": roe
                    }

                    # Calculate YoY Growth
                    prev_years = list(roe_history["standalone"].keys())
                    if prev_years:
                        prev_year = prev_years[-1]
                        prev_roe = roe_history["standalone"][prev_year]

                        if prev_roe and prev_roe != 0:
                            yoy_growth = ((roe - prev_roe) / abs(prev_roe)) * 100
                        else:
                            yoy_growth = None

                        company_result["financials"][year]["standalone"]["yoy_growth"] = yoy_growth

                    # Store ROE for future YoY calculation
                    roe_history["standalone"][year] = roe

                # Process Consolidated
                if "consolidated" in financials[year]:
                    data = financials[year]["consolidated"]
                    try:
                        profit_loss = float(data.get("profit_loss", "N/A"))
                        networth = float(data.get("networth", "N/A"))

                        if networth != 0:
                            roe = (profit_loss / networth) * 100
                        else:
                            roe = None  # Avoid division by zero

                    except ValueError:
                        roe = None  # Invalid data

                    company_result["financials"][year]["consolidated"] = {
                        "profit_loss": data.get("profit_loss", "N/A"),
                        "networth": data.get("networth", "N/A"),
                        "roe": roe
                    }

                    # Calculate YoY Growth
                    prev_years = list(roe_history["consolidated"].keys())
                    if prev_years:
                        prev_year = prev_years[-1]
                        prev_roe = roe_history["consolidated"][prev_year]

                        if prev_roe and prev_roe != 0:
                            yoy_growth = ((roe - prev_roe) / abs(prev_roe)) * 100
                        else:
                            yoy_growth = None

                        company_result["financials"][year]["consolidated"]["yoy_growth"] = yoy_growth

                    # Store ROE for future YoY calculation
                    roe_history["consolidated"][year] = roe

            results.append(company_result)

        # Ensure output directory exists
        os.makedirs(output_directory, exist_ok=True)

        # Save the results to JSON
        with open(output_file_path, "w") as outfile:
            json.dump(results, outfile, indent=4)

    except Exception as e:
        print(f"Error reading or processing data: {e}")

# Run the function
calculate_roe_yoy()
