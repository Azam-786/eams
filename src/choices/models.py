from django.db import models
# from .enums import asset_type_choices, asset_detail_choices, model_choices

class AssetType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class AssetDetail(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Model(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class AssetConfiguration(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Designation(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

    
