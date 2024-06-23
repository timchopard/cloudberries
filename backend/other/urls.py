from django.urls import path 
from . import views
from .views import MdHtmlView, MdParsed

urlpatterns = [
    path("", views.other_index, name="other_index"),
    path("internship/", views.internship, name="other_internship"),
    path("parser/", MdHtmlView.as_view(), name="other_parser"),
    path("parsed/", MdParsed.as_view(), name="other_parsed")
]

