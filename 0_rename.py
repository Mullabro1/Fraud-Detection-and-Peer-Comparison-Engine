import os
import shutil

def rename_xlsx_to_1():
    # Get the script's directory
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Define the input folder and target file path
    input_folder = os.path.join(script_directory, "test")
    target_file = os.path.join(input_folder, "1.xlsx")

    # Ensure the input folder exists
    if not os.path.exists(input_folder):
        print(f"The folder '{input_folder}' does not exist.")
        return

    # Find the first .xlsx file in the input folder
    xlsx_files = [file for file in os.listdir(input_folder) if file.endswith(".xlsx") and file != "1.xlsx"]
    
    if not xlsx_files:
        print("No .xlsx file found in the input folder to rename.")
        return

    # Get the first .xlsx file
    source_file = os.path.join(input_folder, xlsx_files[0])

    # Rename the file to 1.xlsx
    try:
        # Overwrite if 1.xlsx already exists
        if os.path.exists(target_file):
            os.remove(target_file)
        shutil.move(source_file, target_file)
        print(f"Renamed '{xlsx_files[0]}' to '1.xlsx'.")
    except Exception as e:
        print(f"An error occurred while renaming the file: {e}")

# Call the function to rename the file
rename_xlsx_to_1()
