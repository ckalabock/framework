"""Root URL configuration for the visitor accounting application."""

from django.urls import include, path


urlpatterns = [path("", include("webapp.urls"))]
