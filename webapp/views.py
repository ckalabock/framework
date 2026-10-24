"""Views that display the JSON-backed object model from practical work 3."""

from django.http import Http404
from django.shortcuts import render

from storage import load_access_passes, load_employees, load_visitors, load_visits


def load_domain_data():
    """Load all related objects from JSON without using the Django ORM."""
    visitors = load_visitors()
    employees = load_employees()
    access_passes = load_access_passes(visitors)
    visits = load_visits(visitors, employees, access_passes)
    return visitors, employees, access_passes, visits


def find_by_id(items, attribute, item_id):
    """Find an object by its domain identifier or return a standard 404 page."""
    for item in items:
        if getattr(item, attribute) == item_id:
            return item
    raise Http404("Запись не найдена.")


def index(request):
    """Show the start page and compact project statistics."""
    visitors, employees, access_passes, visits = load_domain_data()
    return render(
        request,
        "webapp/home.html",
        {
            "visitor_count": len(visitors),
            "employee_count": len(employees),
            "pass_count": len(access_passes),
            "visit_count": len(visits),
        },
    )


def visitor_list(request):
    """Display every visitor loaded from data/visitors.json."""
    visitors, _, _, _ = load_domain_data()
    return render(request, "webapp/visitors/list.html", {"visitors": visitors})


def visitor_detail(request, visitor_id):
    """Display one visitor and their access passes."""
    visitors, _, access_passes, visits = load_domain_data()
    visitor = find_by_id(visitors, "visitor_id", visitor_id)
    return render(
        request,
        "webapp/visitors/detail.html",
        {
            "visitor": visitor,
            "access_passes": [item for item in access_passes if item.visitor == visitor],
            "visits": [item for item in visits if item.visitor == visitor],
        },
    )


def employee_list(request):
    """Display every employee."""
    _, employees, _, _ = load_domain_data()
    return render(request, "webapp/employees/list.html", {"employees": employees})


def employee_detail(request, employee_id):
    """Display one employee and assigned visits."""
    _, employees, _, visits = load_domain_data()
    employee = find_by_id(employees, "employee_id", employee_id)
    return render(
        request,
        "webapp/employees/detail.html",
        {"employee": employee, "visits": [item for item in visits if item.employee == employee]},
    )


def pass_list(request):
    """Display all issued access passes."""
    _, _, access_passes, _ = load_domain_data()
    return render(request, "webapp/passes/list.html", {"access_passes": access_passes})


def visit_list(request):
    """Display all registered visits."""
    _, _, _, visits = load_domain_data()
    return render(request, "webapp/visits/list.html", {"visits": visits})


def visit_detail(request, visit_id):
    """Display a visit by the dynamic identifier from the URL."""
    _, _, _, visits = load_domain_data()
    visit = find_by_id(visits, "visit_id", visit_id)
    return render(request, "webapp/visits/detail.html", {"visit": visit})
