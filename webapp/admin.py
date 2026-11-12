"""Django Admin configuration for the visitor accounting models (ПР10)."""

from django.contrib import admin

from .models import AccessPass, Employee, Visit, Visitor


class VisitInline(admin.TabularInline):
    model = Visit
    extra = 0
    fields = ("visit_date", "employee", "access_pass", "purpose", "status")
    autocomplete_fields = ("employee", "access_pass")


class AccessPassInline(admin.TabularInline):
    model = AccessPass
    extra = 0
    fields = ("number", "expires_on")


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "document")
    search_fields = ("full_name", "document")
    ordering = ("full_name",)
    inlines = (AccessPassInline, VisitInline)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "department", "is_available")
    list_filter = ("is_available", "department")
    search_fields = ("full_name", "department")
    ordering = ("full_name",)
    inlines = (VisitInline,)


@admin.register(AccessPass)
class AccessPassAdmin(admin.ModelAdmin):
    list_display = ("number", "visitor", "expires_on")
    list_filter = ("expires_on",)
    search_fields = ("number", "visitor__full_name")
    list_select_related = ("visitor",)


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ("id", "visit_date", "visitor", "employee", "access_pass", "status")
    list_filter = ("status", "visit_date", "employee")
    search_fields = ("visitor__full_name", "employee__full_name", "purpose", "access_pass__number")
    list_select_related = ("visitor", "employee", "access_pass")
    autocomplete_fields = ("visitor", "employee", "access_pass")
