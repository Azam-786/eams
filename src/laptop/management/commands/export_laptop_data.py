import pandas as pd
from django.core.management.base import BaseCommand
from location.models import State, City, Country  # adjust if needed
from django.db import transaction
import os
from django.conf import settings
from choices.models import (
    AssetType,
    AssetDetail,
    Model,
    AssetConfiguration,
    Vendor,
    Designation,
)
from laptop.models import Laptop
import pandas as pd
import datetime
from django.conf import settings
import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Export laptop data to CSV"

    def handle(self, *args, **options):
        laptops = Laptop.objects.all().select_related('asset_type', 'asset_details', 'model', 'asset_configuration', 'vendor', 'designation', 'state', 'location')
        data = []
        for index, laptop in enumerate(laptops):
            data.append({
                'index': index + 1,
                'state': laptop.state.name,
                'city': laptop.location.name,
                'asset_type': laptop.asset_type.name,
                'asset_detail': laptop.asset_details.name,
                'asset_tag': laptop.asset_tag,
                'model': laptop.model.name,
                'asset_configuration': laptop.asset_configuration.name,
                'laptop_serial_number': laptop.serial_number,
                'vendor': laptop.vendor.name,
                'employee_name': laptop.employee_name,
                'designation': laptop.designation.name,
                'POD': laptop.pod_number,
                'delivery_status': laptop.delivery_status,
                'admin_user': laptop.admin_user,
                'amount': laptop.amount,
                'gst': laptop.gst,
                'total_amount': laptop.total_amount,
                'invoice_number': laptop.invoice_number,
                'warranty_start_date': laptop.warranty_start_date,
            })
        df = pd.DataFrame(data)
        df.to_csv("laptop/resource/laptop_data.xlsx", index=False)
        print("Laptop data exported to laptop_data.xlsx")


# python manage.py export_laptop_data