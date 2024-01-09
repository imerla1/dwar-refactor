from typing import Any
import json


def read_json(filename: str) -> Any:
    """
    Read a JSON file and return the parsed JSON data.

    Args:
        filename (str): The path to the JSON file.

    Returns:
        Any: The parsed JSON data.
    """
    try:
        with open(filename, mode="r", encoding="utf-8") as json_file:
            json_data = json.load(json_file)
        return json_data

    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{filename}' does not exist.")
    except json.JSONDecodeError as json_error:
        raise ValueError(f"Error decoding JSON in '{filename}': {json_error}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")
