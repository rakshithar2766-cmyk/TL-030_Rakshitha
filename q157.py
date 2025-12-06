import json
raw_data = {
    "Config": {
        "Site": "Bangalore",
        "Devices": 12,
        }
}
def normalize_dict(data):
    new_dict = {}
    for key, value in data.items():
        clean_key = key.lower()

        if isinstance(value, dict):
            new_dict[clean_key] = normalize_dict(value)
        else:
            new_dict[clean_key] = value
    return new_dict

cleaned = normalize_dict(raw_data)
with open("output.json", "w") as f:
    json.dump(cleaned, f, indent=4)
