import json
import csv

with open("normalized_output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

headers = [
    "permit_number", "permit_type_code", "permit_type_description", "permit_class",
    "permit_class_mapped", "permit_work_class",
    "status_current", "status_date",
    "applied_date", "issue_date", "expiration_date", "completion_date",
    "day_issued", "calendar_year", "fiscal_year", "issued_last_30_days",
    "method_issued", "description", "project_id", "master_permit_number",
    "permit_link", "location_address", "location_city", "location_state", "location_zip",
    "location_jurisdiction", "location_council_district", "location_latitude", "location_longitude",
    "property_tcad_id", "property_legal_description"
]

with open("normalized_output.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)

    for rec in data:
        p = rec.get("permit", {})
        l = rec.get("location", {})
        pr = rec.get("property", {})
        s = p.get("status", {})
        c = l.get("coordinates", {})  # <- extract from location.coordinates

        writer.writerow([
            p.get("number"),
            p.get("type_code"),
            p.get("type_description"),
            p.get("class"),
            p.get("class_mapped"),
            p.get("work_class"),
            s.get("current"),
            s.get("date"),
            p.get("applied_date"),
            p.get("issue_date"),
            p.get("expiration_date"),
            p.get("completion_date"),
            p.get("day_issued"),
            p.get("calendar_year"),
            p.get("fiscal_year"),
            p.get("issued_in_last_30_days"),
            p.get("method_issued"),
            p.get("description"),
            p.get("project_id"),
            p.get("master_permit_number"),
            p.get("link"),
            l.get("address"),
            l.get("city"),
            l.get("state"),
            l.get("zip"),
            l.get("jurisdiction"),
            l.get("council_district"),
            c.get("latitude"),
            c.get("longitude"),
            pr.get("tcad_id"),
            pr.get("legal_description")
        ])
