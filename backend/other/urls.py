from django.urls import path 
from . import views

urlpatterns = [
    path("", views.other_index, name="other_index"),
    path("internship/", views.internship, name="other_internship"),
    path("gas/", views.gas, name="other_gas"),
]

