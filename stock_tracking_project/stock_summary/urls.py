from django.urls import path
from . import views

urlpatterns = [
    path("", views.stock_summary_index, name="stock_summary_index"),
]