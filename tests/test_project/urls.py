from django.urls import path, include

import atomicserver.urls

urlpatterns = [
    path("atomic/", include(atomicserver.urls)),
]
