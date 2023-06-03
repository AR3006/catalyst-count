from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(CSVData)
class MeetingAdmin(admin.ModelAdmin):
    list_display = [
        'keyword_number',
        'name',
        'domain',
        'year_founded',
        'industry',
        'size_range',
        'locality',
        'country',
        'linkedin_url',
        'current_employee_estimate',
        'total_employee_estimate',
    ]