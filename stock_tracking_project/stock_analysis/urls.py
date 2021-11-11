from django.urls import path
from . import views

urlpatterns = [
    path("", views.analyzer_index, name="analyzer_index"),
]