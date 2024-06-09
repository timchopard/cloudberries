from django.urls import path 

from . import views 

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
]
