from django.urls import path 
from . import views
from .views import MdHtmlView

urlpatterns = [
    path("", views.other_index, name="other_index"),
    path("internship/", views.internship, name="other_internship"),
    path("mdhtml/", MdHtmlView.as_view(), name="other_parser"),
]

