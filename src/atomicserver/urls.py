from django.urls import path

from atomicserver import views

urlpatterns = [
    path("begin/", views.begin, name="begin"),
    path("rollback/", views.rollback, name="rollback"),
]
