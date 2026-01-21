import csv

with open(
    "static/data/csv/political_violence_events_clean.csv", newline="", encoding="utf-8"
) as f:
    reader = csv.DictReader(f)
    print(reader.fieldnames)
