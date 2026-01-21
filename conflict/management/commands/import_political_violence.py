import csv
from django.core.management.base import BaseCommand
from conflict.models import PoliticalViolenceAdm1Monthly
from regions.models import adm1


class Command(BaseCommand):
    help = "Import political violence CSV data into PoliticalViolenceAdm1Monthly"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the CSV file")
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete all existing PoliticalViolenceAdm1Monthly records before import",
        )

    def handle(self, *args, **options):
        csv_file = options["csv_file"]

        if options["reset"]:
            PoliticalViolenceAdm1Monthly.objects.all().delete()
            self.stdout.write(self.style.WARNING("Deleted all existing records."))

        total_rows = 0
        imported_rows = 0
        skipped_rows = 0
        province_totals = {}

        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                total_rows += 1

                # Clean the column names (remove BOM if present)
                province_name = row.get("\ufeffProvince") or row.get("Province")
                province_name = province_name.strip() if province_name else None
                month_str = row["Month"].strip()
                year = int(row["Year"].strip())
                events = int(row["Events"].strip())
                fatalities = int(row["Fatalities"].strip())

                if not province_name:
                    skipped_rows += 1
                    continue

                try:
                    province_obj = adm1.objects.get(shapename2__iexact=province_name)
                except adm1.DoesNotExist:
                    skipped_rows += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"Skipped row {total_rows}: Province '{province_name}' not found"
                        )
                    )
                    continue

                # Convert month name to number
                month_number = {
                    "January": 1,
                    "February": 2,
                    "March": 3,
                    "April": 4,
                    "May": 5,
                    "June": 6,
                    "July": 7,
                    "August": 8,
                    "September": 9,
                    "October": 10,
                    "November": 11,
                    "December": 12,
                }.get(month_str, 0)

                if month_number == 0:
                    skipped_rows += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"Skipped row {total_rows}: Invalid month '{month_str}'"
                        )
                    )
                    continue

                # Create the record
                PoliticalViolenceAdm1Monthly.objects.create(
                    province=province_obj,
                    month=month_number,
                    year=year,
                    events=events,
                    fatalities=fatalities,
                )

                imported_rows += 1
                province_totals[province_name] = (
                    province_totals.get(province_name, 0) + 1
                )

                if total_rows % 1000 == 0:
                    self.stdout.write(f"Processed {total_rows} rows...")

        self.stdout.write(self.style.SUCCESS(f"Total rows in file: {total_rows}"))
        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported: {imported_rows} rows")
        )
        self.stdout.write(self.style.WARNING(f"Skipped rows: {skipped_rows}"))
        self.stdout.write(self.style.SUCCESS("Imported rows per province:"))
        for prov, count in province_totals.items():
            self.stdout.write(f"  {prov}: {count}")
