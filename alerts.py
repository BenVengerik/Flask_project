import json

SETTINGS_FILE = "settings.json"

def get_settings():
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "alert_thresholds": "placeholder"
        }

settings = get_settings()
print("Loaded settings:", settings)
