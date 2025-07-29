import json
import yaml
from pathlib import Path
from datetime import datetime

#  Load field mapping from a YAML config file
def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

#  Safely retrieve a nested value using a dot-notated path (e.g., "status.date")
def get_nested_value(data, key_path):
    keys = key_path.split('.')
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return None
    return data

#  Apply the field mapping recursively to a record
def apply_mapping(record, mapping):
    def recurse_map(map_node):
        # If the current mapping node is a dictionary, apply mapping recursively
        if isinstance(map_node, dict):
            return {k: recurse_map(v) for k, v in map_node.items()}
        # If it's a string, treat it as a key path to extract from the original record
        elif isinstance(map_node, str):
            return get_nested_value(record, map_node)
        # Otherwise (unexpected type), return None
        return None

    return recurse_map(mapping)

#  Normalize and format date fields in a record
def normalize_dates(data):
    def format_date(date_str):
        if not date_str:
            return None
        try:
            # Attempt to parse ISO format date string and return just the date part (YYYY-MM-DD)
            return datetime.fromisoformat(date_str).date().isoformat()
        except:
            return date_str  # If parsing fails, return the original value

    # List of expected date fields (can include nested fields using dot notation)
    date_fields = [
        "applied_date", "issue_date", "expiration_date",
        "completion_date", "status.date"
    ]

    # Traverse and apply formatting to each date field if it exists
    for field in date_fields:
        keys = field.split(".")
        d = data
        for k in keys[:-1]:
            d = d.get(k, {})
        if keys[-1] in d:
            d[keys[-1]] = format_date(d[keys[-1]])

    return data

#  Main normalization function
def normalize(input_path, output_path, config_path):
    # Load raw JSON records
    with open(input_path, 'r') as f:
        records = json.load(f)

    # Load field mapping from YAML config
    mapping = load_config(config_path)
    normalized = []

    # Apply mapping and date normalization to each record
    for record in records:
        normalized_record = apply_mapping(record, mapping)
        normalized_record = normalize_dates(normalized_record)
        normalized.append(normalized_record)

    # Save the normalized data to output file
    with open(output_path, 'w') as f:
        json.dump(normalized, f, indent=2)

    print(f"✅ Normalized data saved to: {output_path}")

#  Run the pipeline (only when this file is executed directly)
if __name__ == "__main__":
    normalize(
        input_path="austin_permits_sample.json",      # Raw input file
        output_path="normalized_output.json",         # Output location for cleaned data
        config_path="field_mapping.yaml"              # Field mapping config
    )
