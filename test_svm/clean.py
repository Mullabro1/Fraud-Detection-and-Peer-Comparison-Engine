import os
import json

def clean_json(data):
    """Cleans and formats JSON financial data per attribute basis."""
    cleaned_data = []

    for entry in data.get("data", []):  # Ensure handling JSON stored in "data" array
        cleaned_entry = {}

        for key, value in entry.items():
            # Standardize key names: strip whitespace, replace spaces with underscores, lowercase
            new_key = key.strip().replace("\n", "").replace(" ", "_").lower()

            # Preserve important string fields
            if new_key in {"sr.no", "company_name", "f.y._(fin._nature)", "corpository_sector", "product_/_service"}:
                if new_key == "sr.no":
                    cleaned_entry[new_key] = int(value) if str(value).isdigit() else 0  # Ensure sr.no is int
                else:
                    cleaned_entry[new_key] = str(value).strip()  # Keep as string
                continue

            # Convert known missing values to 0
            if value in ["-", "-0", "NULL", "N/A", ""]:
                cleaned_entry[new_key] = 0.0
                continue

            # Handle numeric values (remove commas, percentage signs, and ensure conversion)
            if isinstance(value, str):
                value = value.replace(",", "").replace("%", "").replace("()", "").strip()

                # Convert to float if possible, otherwise keep as string
                try:
                    cleaned_entry[new_key] = float(value) if "." in value else int(value)
                except ValueError:
                    cleaned_entry[new_key] = value  # Keep original value if not numeric
            else:
                cleaned_entry[new_key] = value  # Keep original if it's already numeric

        cleaned_data.append(cleaned_entry)

    return {"data": cleaned_data}  # Maintain the "data" array structure


def process_folder(folder):
    """Processes all JSON files in a given folder and cleans them."""
    script_directory = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(script_directory, folder)

    if not os.path.exists(folder_path):
        print(f"⚠️ Folder '{folder}' not found! Skipping...")
        return

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):  # Ensure only JSON files are processed
            filepath = os.path.join(folder_path, filename)

            try:
                # Read JSON file
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Clean data
                cleaned_data = clean_json(data)

                # Save cleaned JSON
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(cleaned_data, f, indent=4)

                print(f"✅ Cleaned: {filename}")

            except (json.JSONDecodeError, IOError) as e:
                print(f"❌ Error processing {filename}: {e}")


if __name__ == "__main__":
    process_folder("train")
    process_folder("test")
    print("✅ JSON cleaning complete!")
