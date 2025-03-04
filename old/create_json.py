import json
from pathlib import Path


def save_result_as_json(result, file_name):
    """
    Save the result as a JSON file to the desktop.
    """
    desktop_path = Path(r"C:/Users/zohre/OneDrive/Desktop") / file_name

    try:
        with open(desktop_path, "w") as json_file:
            json.dump(result, json_file, indent=4)

        print(f"Result successfully saved to {desktop_path}")

    except Exception as e:
        print(f"Error saving the JSON file: {e}")

