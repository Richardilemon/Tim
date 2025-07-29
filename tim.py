import json
import pandas as pd

# Load the manually saved file
with open("austin_permits_sample.json") as f:
    data = json.load(f)

# Normalize and convert to CSV
df = pd.json_normalize(data)
df.to_csv("austin_permits_sample.csv", index=False)

print("✅ Converted to austin_permits_sample.csv")
