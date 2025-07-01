from django.contrib import admin
from .models import AssetType, AssetDetail, Model, AssetConfiguration, Vendor, Designation

class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

class AssetDetailAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ModelAdmin(admin.ModelAdmin):
    list_display = ('name',)

class AssetConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name',)

class VendorAdmin(admin.ModelAdmin):
    list_display = ('name',)

class DesignationAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(AssetType, AssetTypeAdmin)
admin.site.register(AssetDetail, AssetDetailAdmin)
admin.site.register(Model, ModelAdmin)
admin.site.register(AssetConfiguration, AssetConfigurationAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Designation, DesignationAdmin)