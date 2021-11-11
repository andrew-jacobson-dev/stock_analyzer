from django.contrib import admin
from .models import UserProfile, UserStock, UserStockTransaction, UserStockAlert


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserStock)
admin.site.register(UserStockTransaction)
admin.site.register(UserStockAlert)