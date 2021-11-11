from django.urls import path
from . import views

urlpatterns = [
    path("", views.registration_index, name="registration_index"),
    path("profile", views.profile_index, name="profile_index"),
]