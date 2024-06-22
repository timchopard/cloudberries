from django.urls import path 

from . import views 
from .views import ContactView, SuccessView

urlpatterns = [
    path(
        "", 
        views.cloudberries_index, 
        name="cloudberries_index"
    ),
    path(
        "posts/",
        views.cloudberries_posts,
        name="cloudberries_posts",
    ),
    path(
        "post/<int:pk>/", 
        views.cloudberries_detail, 
        name="cloudberries_detail"
    ),
    path(
        "category/<category>/",
        views.cloudberries_category, 
        name="cloudberries_category"
    ),
    path(
        "contact/",
        ContactView.as_view(),
        name="cloudberries_contact"
    ),
    path(
        "success/",
        SuccessView.as_view(),
        name="success"
    ),
    path(
        "projects/",
        views.cloudberries_projects,
        name="cloudberries_projects"
    ),
    path(
        "tutorials/",
        views.cloudberries_tutorials,
        name="cloudberries_tutorials"
    ),
]
