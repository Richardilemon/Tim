
import json
import psycopg2

# Supabase connection details
conn = psycopg2.connect(
    host="db.ipkotzsdxlwwhqdyqkqn.supabase.co",
    options='-c inet_protocols=ipv4',
    port=5432,
    dbname="postgres",
    user="postgres",
    password="n.NJV_35iWUZF4B"
)

cur = conn.cursor()

# Create table if it doesn't exist (flattened structure)
create_table_sql = """
CREATE TABLE IF NOT EXISTS permits (
    permit_number TEXT,
    permit_class TEXT,
    permit_type TEXT,
    permit_type_desc TEXT,
    work_class TEXT,
    status_current TEXT,
    status_date DATE,
    applied_date DATE,
    issue_date DATE,
    expiration_date DATE,
    completion_date DATE,
    original_address1 TEXT,
    city TEXT,
    state TEXT,
    zip TEXT,
    contractor_name TEXT,
    contractor_license TEXT
);
"""

cur.execute(create_table_sql)
conn.commit()

# Load normalized data
with open("normalized_output.json") as f:
    records = json.load(f)

# Insert records
insert_sql = """
INSERT INTO permits (
    permit_number, permit_class, permit_type, permit_type_desc, work_class,
    status_current, status_date, applied_date, issue_date, expiration_date,
    completion_date, original_address1, city, state, zip,
    contractor_name, contractor_license
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for rec in records:
    status = rec.get("status", {})
    contractor = rec.get("contractor", {})
    location = rec.get("location", {})

    values = (
        rec.get("permit_number"),
        rec.get("permit_class"),
        rec.get("permit_type"),
        rec.get("permit_type_desc"),
        rec.get("work_class"),
        status.get("current"),
        status.get("date"),
        rec.get("applied_date"),
        rec.get("issue_date"),
        rec.get("expiration_date"),
        rec.get("completion_date"),
        location.get("address"),
        location.get("city"),
        location.get("state"),
        location.get("zip"),
        contractor.get("name"),
        contractor.get("license")
    )
    cur.execute(insert_sql, values)

conn.commit()
cur.close()
conn.close()

print("✅ Loaded records into Supabase PostgreSQL")
