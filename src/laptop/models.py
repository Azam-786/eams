from django.db import models
from location.models import State, City
from choices.models import (
    AssetType,
    AssetDetail,
    Model,
    AssetConfiguration,
    Vendor,
    Designation,
)


class Laptop(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    location = models.ForeignKey(City, on_delete=models.CASCADE)
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE)
    asset_details = models.ForeignKey(AssetDetail, on_delete=models.CASCADE)
    asset_tag = models.CharField(max_length=255)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    asset_configuration = models.ForeignKey(
        AssetConfiguration, on_delete=models.CASCADE
    )
    serial_number = models.CharField(max_length=255)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    employee_name = models.CharField(max_length=255)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    pod_number = models.CharField(max_length=255, null=True, blank=True)
    delivery_status = models.CharField(max_length=255)
    admin_user = models.CharField(max_length=255, default="DONE")
    amount = models.IntegerField()
    gst = models.IntegerField()
    total_amount = models.IntegerField()
    invoice_number = models.CharField(max_length=255)
    warranty_start_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.state.name} - {self.location.name}"
