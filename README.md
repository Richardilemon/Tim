# ConstructIQ Data Engineering Challenge

## 📌 Overview

This project focuses on building a robust ETL pipeline for the City of Austin’s building permit dataset. The dataset is provided in JSON format and includes nested, semi-structured data. The goal is to clean, normalize, transform, and store the data in a shareable PostgreSQL database, and optionally expose it via API or visualization.

---

## 🛠️ Technologies Used

- **Python 3**
- **PyYAML** — config-based field mapping
- **psycopg2** — PostgreSQL connector
- **Supabase** — PostgreSQL + REST API hosting
- **Requests** — for API calls and HTTP handling
- **JSON/CSV** — data transformation formats

---

## ✅ Completed Tasks

| Step | Description |
|------|-------------|
| ✅ 1. | Downloaded JSON data from Austin Open Data portal |
| ✅ 2. | Explored and analyzed structure with nested fields |
| ✅ 3. | Normalized nested fields (`status`, `coordinates`, etc.) |
| ✅ 4. | Used `config.yaml` to control and rename fields |
| ✅ 5. | Wrote a transformation pipeline in `normalize.py` |
| ✅ 6. | Exported cleaned data to `normalized_output.csv` |
| ✅ 7. | Loaded data into **Supabase PostgreSQL** |
| ✅ 8. | Made data publicly accessible via Supabase REST API |

---

## 📂 Files

- `normalize.py` — main script to clean and flatten raw data  
- `config.yaml` — field mapping config  
- `export_to_csv.py` — converts cleaned data to CSV  
- `load_to_supabase.py` — (optional) programmatic loader  
- `normalized_output.csv` — clean output uploaded to Supabase  
- `austin_permits_sample.json` — raw input sample  
- `query.py` — to Query the Supabase API

---

## 🌐 Public API Access

You can query the uploaded data directly via Supabase's REST API:


### Schema explanation

While the raw dataset contains 68 fields per record, 
I’ve reviewed all columns and included only those relevant to permit analysis. 
Metadata fields (e.g., :@computed_region_*) and redundant values (e.g., permit_location vs original_address1) were dropped to avoid duplication and noise. 
A full audit table is provided below.



| Original Field               | Normalized Field                          | Included? | Reason                                                         |
| ---------------------------- | ----------------------------------------- | --------- | -------------------------------------------------------------- |
| `permit_number`              | `permit.number`                           | ✅         | Unique identifier for the permit                               |
| `permittype`                 | `permit.type_code`                        | ✅         | Code for permit type (e.g., DS, PP)                            |
| `permit_type_desc`           | `permit.type_description`                 | ✅         | Human-readable description of the permit                       |
| `permit_class`               | `permit.class`                            | ✅         | Specific class like “Residential” or “Com. Sidewalk”           |
| `permit_class_mapped`        | `permit.class_mapped`                     | ✅         | Broad class mapping (used across cities)                       |
| `work_class`                 | `permit.work_class`                       | ✅         | Type of work involved (e.g., “New”, “Repair”)                  |
| `status_current`             | `permit.status.current`                   | ✅         | Current status (e.g., Final, Active)                           |
| `statusdate`                 | `permit.status.date`                      | ✅         | Date when current status was assigned                          |
| `applieddate`                | `permit.applied_date`                     | ✅         | When application was submitted                                 |
| `issue_date`                 | `permit.issue_date`                       | ✅         | Date permit was issued                                         |
| `expiresdate`                | `permit.expiration_date`                  | ✅         | When the permit expires                                        |
| `completed_date`             | `permit.completion_date`                  | ✅         | When the work was completed                                    |
| `day_issued`                 | `permit.day_issued`                       | ✅         | Day of the week (optional but included)                        |
| `calendar_year_issued`       | `permit.calendar_year`                    | ✅         | Useful for reporting across years                              |
| `fiscal_year_issued`         | `permit.fiscal_year`                      | ✅         | Useful for city budgeting                                      |
| `issued_in_last_30_days`     | `permit.issued_in_last_30_days`           | ✅         | Flag for recent activity                                       |
| `issue_method`               | `permit.method_issued`                    | ✅         | How it was issued (e.g., online or in person)                  |
| `description`                | `permit.description`                      | ✅         | Text description of the work                                   |
| `project_id`                 | `permit.project_id`                       | ✅         | Internal tracking number                                       |
| `masterpermitnum`            | `permit.master_permit_number`             | ✅         | Links related permits                                          |
| `link.url`                   | `permit.link`                             | ✅         | Public-facing permit lookup link                               |
| `original_address1`          | `location.address`                        | ✅         | Cleaned address                                                |
| `original_city`              | `location.city`                           | ✅         | City name                                                      |
| `original_state`             | `location.state`                          | ✅         | State abbreviation                                             |
| `original_zip`               | `location.zip`                            | ✅         | ZIP code                                                       |
| `jurisdiction`               | `location.jurisdiction`                   | ✅         | Local authority                                                |
| `council_district`           | `location.council_district`               | ✅         | District representation (if available)                         |
| `latitude`, `longitude`      | `location.coordinates`                    | ✅         | Geolocation grouped as sub-object                              |
| `tcad_id`                    | `property.tcad_id`                        | ✅         | Property ID                                                    |
| `legal_description`          | `property.legal_description`              | ✅         | Parcel description                                             |
| `location.human_address`     | (Dropped)                                 | ❌         | Usually empty or duplicate of better fields                    |
| `permit_location`            | (Dropped in favor of `original_address1`) | ❌         | Duplicates `original_address1`                                 |
| `:@computed_region_*` fields | (Dropped)                                 | ❌         | Computed city regions — not relevant unless doing GIS analysis |



The full table is provided below to ensure transparency

| Raw Field Name                | Kept? | Normalized Field                 | Reason                                      |
| ----------------------------- | ----- | -------------------------------- | ------------------------------------------- |
| `:@computed_region_6gig_z43c` | ❌     |                                  | Dropped: redundant, computed, or not useful |
| `:@computed_region_8spj_utxs` | ❌     |                                  | Dropped: redundant, computed, or not useful |
| `:@computed_region_a3it_2a2z` | ❌     |                                  | Dropped: redundant, computed, or not useful |
| `:@computed_region_e9j2_6w3z` | ❌     |                                  | Dropped: redundant, computed, or not useful |
| `:@computed_region_i2aj_cj5t` | ❌     |                                  | Dropped: redundant, computed, or not useful |
| `:@computed_region_m2th_e4b7` | ❌     |                                  | Dropped: redundant, computed, or not useful |
| `:@computed_region_q9nd_rr82` | ❌     |                                  | Dropped: redundant, computed, or not useful |
| `:@computed_region_qwte_z96m` | ❌     |                                  | Dropped: redundant, computed, or not useful |
| `:@computed_region_rxpj_nzrk` | ❌     |                                  | Dropped: redundant, computed, or not useful |
| `calendar_year_issued`        | ✅     | `permit.calendar_year`           | Mapped to normalized schema                 |
| `completed_date`              | ✅     | `permit.completion_date`         | Mapped to normalized schema                 |
| `council_district`            | ✅     | `location.council_district`      | Mapped to normalized schema                 |
| `day_issued`                  | ✅     | `permit.day_issued`              | Mapped to normalized schema                 |
| `description`                 | ✅     | `permit.description`             | Mapped to normalized schema                 |
| `expiresdate`                 | ✅     | `permit.expiration_date`         | Mapped to normalized schema                 |
| `fiscal_year_issued`          | ✅     | `permit.fiscal_year`             | Mapped to normalized schema                 |
| `issue_date`                  | ✅     | `permit.issue_date`              | Mapped to normalized schema                 |
| `issue_method`                | ✅     | `permit.method_issued`           | Mapped to normalized schema                 |
| `issued_in_last_30_days`      | ✅     | `permit.issued_in_last_30_days`  | Mapped to normalized schema                 |
| `jurisdiction`                | ✅     | `location.jurisdiction`          | Mapped to normalized schema                 |
| `latitude`                    | ✅     | `location.coordinates.latitude`  | Mapped to normalized schema                 |
| `legal_description`           | ✅     | `property.legal_description`     | Mapped to normalized schema                 |
| `link.url`                    | ✅     | `permit.link`                    | Mapped to normalized schema                 |
| `location.human_address`      | ❌     |                                  | Dropped: empty or redundant                 |
| `location.latitude`           | ✅     | `location.coordinates.latitude`  | Mapped to normalized schema                 |
| `location.longitude`          | ✅     | `location.coordinates.longitude` | Mapped to normalized schema                 |
| `longitude`                   | ✅     | `location.coordinates.longitude` | Mapped to normalized schema                 |
| `masterpermitnum`             | ✅     | `permit.master_permit_number`    | Mapped to normalized schema                 |
| `original_address1`           | ✅     | `location.address`               | Mapped to normalized schema                 |
| `original_city`               | ✅     | `location.city`                  | Mapped to normalized schema                 |
| `original_state`              | ✅     | `location.state`                 | Mapped to normalized schema                 |
| `original_zip`                | ✅     | `location.zip`                   | Mapped to normalized schema                 |
| `permit_class`                | ✅     | `permit.class`                   | Mapped to normalized schema                 |
| `permit_class_mapped`         | ✅     | `permit.class_mapped`            | Mapped to normalized schema                 |
| `permit_location`             | ❌     |                                  | Dropped: duplicate of `original_address1`   |
| `permit_number`               | ✅     | `permit.number`                  | Mapped to normalized schema                 |
| `permit_type_desc`            | ✅     | `permit.type_description`        | Mapped to normalized schema                 |
| `permittype`                  | ✅     | `permit.type_code`               | Mapped to normalized schema                 |
| `project_id`                  | ✅     | `permit.project_id`              | Mapped to normalized schema                 |
| `status_current`              | ✅     | `permit.status.current`          | Mapped to normalized schema                 |
| `statusdate`                  | ✅     | `permit.status.date`             | Mapped to normalized schema                 |
| `tcad_id`                     | ✅     | `property.tcad_id`               | Mapped to normalized schema                 |
| `work_class`                  | ✅     | `permit.work_class`              | Mapped to normalized schema                 |


All date fields are converted to ISO format (YYYY-MM-DD)


---
### 🔧 Run Instructions

#### 1. 🐍 Set up a virtual environment (recommended)

```bash
python3 -m venv up
source up/bin/activate  # on Windows: up\Scripts\activate
```

#### 2. 📦 Install dependencies

```bash
pip install -r requirements.txt
```
---

#### 3. 📥 Normalize Raw Data

Transform the original nested JSON data into a flat format:

```bash
python normalize.py
```

This will:

* Load the raw JSON file (`austin_permits_sample.json`)
* Normalize and rename fields using `config.yaml`
* Output a cleaned JSON file (`normalized_output.json`)

---

#### 4. 📤 Export to CSV

Convert the cleaned JSON to a Supabase-ready CSV:

```bash
python export_to_csv.py
```

This creates `normalized_output.csv`.

---

#### 5. 🛠 (Optional) Load to Supabase via Script (Data is already loaded)

```bash
python load_to_supabase.py
```



---

#### 6. 🌐 Query via Supabase REST API

Once loaded, you can access the data at:

```
GET https://<project-ref>.supabase.co/rest/v1/permits
```

With headers:

```
apikey: ANON_KEY
Authorization: Bearer ANON_KEY
```
the details are in query.py
Or just run:

```bash
python query.py
```



### **REST API section**
⚠️ This Supabase instance is provided for demo purposes only.
You can replace the URL and API keys with your own credentials to run this pipeline in your environment.
