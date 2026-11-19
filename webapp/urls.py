"""Named routes for the visitor accounting application."""

from django.urls import path

from . import views


app_name = "webapp"

urlpatterns = [
    path("", views.index, name="index"),
    path("visitors/", views.visitor_list, name="visitor_list"),
    path("visitors/<int:visitor_id>/", views.visitor_detail, name="visitor_detail"),
    path("employees/", views.employee_list, name="employee_list"),
    path("employees/<int:employee_id>/", views.employee_detail, name="employee_detail"),
    path("passes/", views.pass_list, name="pass_list"),
    path("visits/", views.visit_list, name="visit_list"),
    path("visits/create/", views.visit_create, name="visit_create"),
    path("visits/<int:visit_id>/", views.visit_detail, name="visit_detail"),
    path("visits/<int:visit_id>/edit/", views.visit_edit, name="visit_edit"),
    path("visits/<int:visit_id>/cancel/", views.visit_cancel, name="visit_cancel"),
]
