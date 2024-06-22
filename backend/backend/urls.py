from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("cloudberries.urls")),
    # path("llm/", include("llm.urls")),
    # path("bernimprov/", include("bernimprov.urls")),
]
