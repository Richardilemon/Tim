import requests


PROJECT_REF = "ipkotzsdxlwwhqdyqkqn"
TABLE_NAME = "permits"

url = f"https://{PROJECT_REF}.supabase.co/rest/v1/{TABLE_NAME}"

headers = {
    "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlwa290enNkeGx3d2hxZHlxa3FuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM3Mjc5MzUsImV4cCI6MjA2OTMwMzkzNX0.OxXtvlkM1kElOy0J8Z07rGTdKw6QjJQq5lDkgbCH3Wk",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlwa290enNkeGx3d2hxZHlxa3FuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM3Mjc5MzUsImV4cCI6MjA2OTMwMzkzNX0.OxXtvlkM1kElOy0J8Z07rGTdKw6QjJQq5lDkgbCH3Wk"
}

params = {
    "select": "*",
    "limit": 10
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    print("✅ Success! Sample data:")
    for row in response.json():
        print(row)
else:
    print(f"❌ Failed: {response.status_code} - {response.text}")
