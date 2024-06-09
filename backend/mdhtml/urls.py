from django.urls import path 

from . import views 

urlpatterns = [
    path(
        "", 
        views.md_to_html,
        name="md_to_html",
    ),
]
