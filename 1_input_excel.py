import os
import pandas as pd

# Get the script's directory
script_directory = os.path.dirname(os.path.abspath(__file__))

# Define the input file (1.xlsx) and output folder
input_file = os.path.join(script_directory, "test", "1.xlsx")
output_folder = os.path.join(script_directory, "exl")

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Check if the input file exists
if not os.path.exists(input_file):
    print(f"Error: Input file not found at {input_file}")
    exit()

# Process the input file
print(f"Processing file: {input_file}")

# Load the workbook using pandas
excel_file = pd.ExcelFile(input_file)

# Get all sheet names
sheet_names = excel_file.sheet_names
print("Sheets detected:", sheet_names)

# Loop through all sheets in the Excel file
for sheet_name in sheet_names:
    print(f"Processing sheet: {sheet_name}")

    # Read the sheet
    df = pd.read_excel(input_file, sheet_name=sheet_name)
    
    # Save the sheet directly into the output folder
    output_file = os.path.join(output_folder, f"{sheet_name}.xlsx")
    df.to_excel(output_file, index=False)
    print(f"Saved sheet '{sheet_name}' to: {output_file}")

print(f"Finished processing file: {input_file}")
