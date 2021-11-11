from django.contrib import admin
from .models import Stock, StockRecommendation, SectorIndustryPerformance, StockEOD, StockEODProfile

# Register your models here.
admin.site.register(Stock)
admin.site.register(StockRecommendation)
admin.site.register(SectorIndustryPerformance)
admin.site.register(StockEOD)
admin.site.register(StockEODProfile)