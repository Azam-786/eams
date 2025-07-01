from django.contrib import admin
from .models import State, City, Country

class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')

admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)    
admin.site.register(Country, CountryAdmin)