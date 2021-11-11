from django.contrib import admin
from .models import NYSEHoliday, JobRun

# Register your models here.
admin.site.register(NYSEHoliday)
admin.site.register(JobRun)