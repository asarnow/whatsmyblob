## Blobapp urls

from blobapp import views
from django.urls import path, include

urlpatterns = [
    path('', views.handle_req),
]