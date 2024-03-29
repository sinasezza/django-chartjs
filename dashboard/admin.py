from django.contrib import admin
from .models import CountryData

@admin.register(CountryData)
class CountryDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'population',)