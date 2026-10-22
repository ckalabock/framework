"""URLs for HTML pages and JSON API."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("visitors/new/", views.create_visitor, name="create_visitor"),
    path("employees/new/", views.create_employee, name="create_employee"),
    path("passes/new/", views.create_pass, name="create_pass"),
    path("visits/new/", views.create_visit, name="create_visit"),
    path("visits/<int:visit_id>/cancel/", views.cancel_visit, name="cancel_visit"),
    path("api/visitors/", views.visitors_api, name="visitors_api"),
    path("api/visits/", views.visits_api, name="visits_api"),
]
