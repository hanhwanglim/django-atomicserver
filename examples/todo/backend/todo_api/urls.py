from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path("tasks/", include("tasks.urls")),
]

if settings.ENV == "CI":
    urlpatterns.append(path("atomic/", include("atomicserver.urls")))
