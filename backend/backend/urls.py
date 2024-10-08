from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("cloudberries.urls")),
    path("other/", include("other.urls")),
    path('captcha/', include('captcha.urls')),
]
