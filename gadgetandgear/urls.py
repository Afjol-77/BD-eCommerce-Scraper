from django.urls import path
from . import views


urlpatterns = [
    path('', views.gadgetandgear, name="gng"),
]