import pandas as pd
from django.core.management.base import BaseCommand
from location.models import State, City, Country  # adjust if needed
from django.db import transaction
import os
from django.conf import settings
from choices.models import AssetType, AssetDetail, Model, AssetConfiguration, Vendor, Designation
from laptop.models import Laptop
import pandas as pd
import datetime
from django.conf import settings
import os
from django.core.management.base import BaseCommand

# return all values in dict
def get_value_from_row(row, column_name):
    hash_map = {}
    for col, val in row.items():
        hash_map[col] = val
    return hash_map

def get_total_amount(number):
    if type(number) == int:
        return number
    if type(number) == float:
        return int(number)
    if ',' in number:
        number = number.replace(',', '')
    return int(number)


def parse_excel_date(value):
    if pd.isna(value):  # Handles NaT or NaN
        return None
    if isinstance(value, datetime.datetime) or isinstance(value, datetime.date):
        return value
    try:
        return pd.to_datetime(value)
    except Exception:
        return None


class Command(BaseCommand):
    help = "Import state and city data from CSV"

    def handle(self, *args, **options):
        csv_file = "laptop/resource/IT Tracker 26-06.xlsx"
        excel_file_path = os.path.join(settings.BASE_DIR, csv_file)
        try:
            df = pd.read_excel(excel_file_path, engine="openpyxl")  # or 'xlrd' for .xls
            # df = pd.read_excel(excel_file_path, engine="xlrd")
        except Exception as e:
            self.stderr.write(f"Failed to read Excel file: {e}")
            return

        # print(df.columns)
        required_columns = {
            "No",
            "State",
            " Location",
            "Asset Type",
            "Asset Details",
            "Asset Tag",
            "Model",
            "Asset Configuration",
            "Serial No",
            "Vendor",
            "EMP NAME",
            "Designation",
            "POD NO",
            "Delivery Status",
            "Admin User",
            "Amount ",
            "GST",
            "Total ",
            "Purchase date",
            "Invoice No",
            "warrenty start as per PRODUCT",
            "Warrenty expire",
            "day remaing for expire",
            "MS OFFICE LICENSE",
            "LICENSE Invoice no",
            "MS OFFICE EXPIRE",
            "Admin password",
        }

        if not required_columns.issubset(df.columns):
            self.stderr.write(f"Excel must contain these columns: {required_columns}")
            return
        try:
            for index, row in df.iterrows():
                values = get_value_from_row(row, required_columns)
                state_instance, _ = State.objects.get_or_create(name=values.pop('State'))
                location_instance, _ = City.objects.get_or_create(name=values.pop(' Location'), state=state_instance)
                asset_type_instance, _ = AssetType.objects.get_or_create(name=values.pop('Asset Type'))
                asset_detail_instance, _ = AssetDetail.objects.get_or_create(name=values.pop('Asset Details'))
                model_instance, _ = Model.objects.get_or_create(name=values.pop('Model'))
                asset_configuration_instance, _ = AssetConfiguration.objects.get_or_create(name=values.pop('Asset Configuration'))
                vendor_instance, _ = Vendor.objects.get_or_create(name=values.pop('Vendor'))
                designation_instance, _ = Designation.objects.get_or_create(name=values.pop('Designation'))
                pod_number = values.pop('POD NO')
                asset_tag = values.pop('Asset Tag')
                serial_number = values.pop('Serial No')
                purchase_date = parse_excel_date(values.pop('Purchase date'))
                invoice_number = values.pop('Invoice No')
                warranty_start_date = parse_excel_date(values.pop('warrenty start as per PRODUCT'))
                warranty_expire_date = parse_excel_date(values.pop('Warrenty expire'))
                day_remaining_for_expire = values.pop('day remaing for expire')
                employee_name = values.pop('EMP NAME')
                admin_user = values.pop('Admin User')
                amount = get_total_amount(values.pop("Amount "))
                gst = get_total_amount(values.pop("GST"))
                total_amount = get_total_amount(values.pop("Total "))
                delivery_status = values.pop('Delivery Status')

                laptop_instance, _ = Laptop.objects.get_or_create(
                    state=state_instance,
                    location=location_instance,
                    asset_type=asset_type_instance,
                    asset_details=asset_detail_instance,
                    asset_tag=asset_tag,
                    serial_number=serial_number,
                    model=model_instance,
                    asset_configuration=asset_configuration_instance,
                    vendor=vendor_instance,
                    employee_name=employee_name,
                    designation=designation_instance,
                    pod_number=pod_number,
                    delivery_status=delivery_status,
                    admin_user=admin_user,
                    amount=amount,
                    gst=gst,
                    total_amount=total_amount,
                    invoice_number=invoice_number,
                    warranty_start_date=warranty_start_date,
                )
        except Exception as e:
            print(f"Error creating laptop {index+1}: {e}")
            # continue
        print(f"Laptop {index+1} created")
        # if index == 5:
        #     break


# python manage.py import_laptop_data
