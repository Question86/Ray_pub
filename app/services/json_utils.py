import json

def load_profiles(file_path="C:\\Users\\ambas\\Ray\\app\\data\\profiles.json"):
    """
    Lädt die JSON-Datei und gibt die Daten zurück.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"{file_path} not found")
    except json.JSONDecodeError:
        raise ValueError(f"{file_path} is not a valid JSON file")

def filter_profiles(data, profile_type: str):
    """
    Filtert die Profile basierend auf dem Typ (z. B. user_profile).
    """
    return [entry for entry in data if entry["type"] == profile_type]
