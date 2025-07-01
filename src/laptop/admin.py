from django.contrib import admin
from .models import Laptop


class LaptopAdmin(admin.ModelAdmin):
    list_display = (
        "state",
        "location",
        "asset_type",
        "asset_details",
        "asset_tag",
        "model",
        "asset_configuration",
        "serial_number",
        "vendor",
        "employee_name",
        "designation",
        "pod_number",
        "delivery_status",
        "admin_user",
        "amount",
        "gst",
        "total_amount",
        "invoice_number",
        "warranty_start_date",
    )
    search_fields = ("state__name", "location__name", "asset_tag", "serial_number")


admin.site.register(Laptop, LaptopAdmin)
