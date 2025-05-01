import pandas as pd
import os
import re

# Get the script's directory
script_directory = os.path.dirname(os.path.abspath(__file__))

# Define input and output folders
input_folder = os.path.join(script_directory, "exl")
output_folder = os.path.join(script_directory, "test")
output_file = os.path.join(output_folder, "merged_output.xlsx")

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Function to extract number from filename
def extract_number(filename):
    match = re.search(r'Table (\d+)', filename)  # Extracts the number after "Table "
    return int(match.group(1)) if match else float('inf')  # If no number, put it last

# List and sort Excel files numerically
excel_files = sorted(
    [f for f in os.listdir(input_folder) if f.endswith(".xlsx")],
    key=extract_number
)

# Define the fixed DataFrame shape
ROWS, COLS = 60, 60

# Initialize a list to store DataFrames
df_list = []

# Read each Excel file and process
for file in excel_files:
    file_path = os.path.join(input_folder, file)
    df = pd.read_excel(file_path, header=None, dtype=str)  # Read as text

    # Ensure df is exactly 100x100 (truncate or pad with empty strings)
    df = df.reindex(index=range(ROWS), columns=range(COLS), fill_value="")

    # Create a header row with the filename in the first column
    header_row = pd.DataFrame([[file] + [""] * (COLS - 1)], columns=range(COLS))

    # Append the header row and the DataFrame
    df_list.append(header_row)
    df_list.append(df)

# Combine all DataFrames vertically
merged_df = pd.concat(df_list, ignore_index=True)

# Save merged DataFrame to an Excel file
merged_df.to_excel(output_file, index=False, header=False)

print(f"Merged {len(excel_files)} files in numerical order and saved to {output_file}")
