
import json
import yaml
from pathlib import Path
from datetime import datetime

def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_nested_value(data, key_path):
    keys = key_path.split('.')
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return None
    return data

def apply_mapping(record, mapping):
    def recurse_map(map_node):
        if isinstance(map_node, dict):
            return {k: recurse_map(v) for k, v in map_node.items()}
        elif isinstance(map_node, str):
            return get_nested_value(record, map_node)
        return None

    return recurse_map(mapping)

def normalize_dates(data):
    def format_date(date_str):
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str).date().isoformat()
        except:
            return date_str

    date_fields = [
        "applied_date", "issue_date", "expiration_date",
        "completion_date", "status.date"
    ]

    for field in date_fields:
        keys = field.split(".")
        d = data
        for k in keys[:-1]:
            d = d.get(k, {})
        if keys[-1] in d:
            d[keys[-1]] = format_date(d[keys[-1]])

    return data

def normalize(input_path, output_path, config_path):
    with open(input_path, 'r') as f:
        records = json.load(f)

    mapping = load_config(config_path)
    normalized = []

    for record in records:
        normalized_record = apply_mapping(record, mapping)
        normalized_record = normalize_dates(normalized_record)
        normalized.append(normalized_record)

    with open(output_path, 'w') as f:
        json.dump(normalized, f, indent=2)
    print(f"✅ Normalized data saved to: {output_path}")

if __name__ == "__main__":
    normalize(
        input_path="austin_permits_sample.json",
        output_path="normalized_output.json",
        config_path="field_mapping.yaml"
    )
