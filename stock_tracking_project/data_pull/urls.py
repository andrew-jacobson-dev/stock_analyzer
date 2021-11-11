from django.urls import path
from . import views

urlpatterns = [
    path("jobs", views.jobs_index, name="jobs_index"),
]