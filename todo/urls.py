from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/toggle/", views.toggle, name="toggle"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("health/", views.health, name="health"),
]
