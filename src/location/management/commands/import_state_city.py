import pandas as pd
from django.core.management.base import BaseCommand
from location.models import State, City, Country  # adjust if needed
from django.db import transaction
import os
from django.conf import settings


class Command(BaseCommand):
    help = "Import state and city data from CSV"

    def handle(self, *args, **options):
        csv_file = "location/resource/data.xlsx"
        excel_file_path = os.path.join(settings.BASE_DIR, csv_file)
        try:
            df = pd.read_excel(excel_file_path, engine="openpyxl")  # or 'xlrd' for .xls
            # df = pd.read_excel(excel_file_path, engine="xlrd")
        except Exception as e:
            self.stderr.write(f"Failed to read Excel file: {e}")
            return

        required_columns = {"State", "City"}

        if not required_columns.issubset(df.columns):
            self.stderr.write(f"Excel must contain these columns: {required_columns}")
            return

        country, _ = Country.objects.get_or_create(
            name="India", defaults={"code": "IN"}
        )

        # Step 2: Normalize data
        df["State"] = df["State"].astype(str).str.strip()
        df["City"] = df["City"].astype(str).str.strip()
        state_names = df["State"].unique()

        # Step 3: Fetch existing states
        existing_states = State.objects.filter(name__in=state_names, country=country)
        state_map = {s.name: s for s in existing_states}

        # Step 4: Create missing states
        missing_states = [
            State(name=name, country=country)
            for name in state_names
            if name not in state_map
        ]
        State.objects.bulk_create(missing_states)
        self.stdout.write(f"✅ Created {len(missing_states)} new states")

        # Refresh state_map with new entries
        all_states = State.objects.filter(name__in=state_names, country=country)
        state_map = {s.name: s for s in all_states}

        # Step 5: Fetch existing cities
        existing_cities = City.objects.all().values_list("name", "state_id")
        existing_city_set = set((name, state_id) for name, state_id in existing_cities)

        # Step 6: Create missing cities
        new_cities = []
        for _, row in df.iterrows():
            state = state_map[row["State"]]
            city_key = (row["City"], state.id)
            if city_key not in existing_city_set:
                new_cities.append(City(name=row["City"], state=state))
                existing_city_set.add(city_key)

        City.objects.bulk_create(new_cities)
        self.stdout.write(f"✅ Created {len(new_cities)} new cities")

        self.stdout.write(self.style.SUCCESS("🎉 Import complete with bulk insert."))


# python manage.py import_state_city