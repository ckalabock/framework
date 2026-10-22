"""HTML views and a small JSON API for visitor accounting."""

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AccessPassForm, EmployeeForm, VisitForm, VisitorForm
from .models import AccessPassRecord, EmployeeRecord, VisitRecord, VisitorRecord


@login_required
def dashboard(request):
    """Show the dashboard with current visitors and visits."""
    context = {
        "visitors": VisitorRecord.objects.all(),
        "employees": EmployeeRecord.objects.all(),
        "passes": AccessPassRecord.objects.select_related("visitor"),
        "visits": VisitRecord.objects.select_related("visitor", "employee", "access_pass"),
    }
    return render(request, "webapp/dashboard.html", context)


@login_required
def create_visitor(request):
    """Create a visitor from a validated form."""
    form = VisitorForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("dashboard")
    return render(request, "webapp/form.html", {"form": form, "title": "Новый посетитель"})


@login_required
def create_employee(request):
    """Create an employee from a validated form."""
    form = EmployeeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("dashboard")
    return render(request, "webapp/form.html", {"form": form, "title": "Новый сотрудник"})


@login_required
def create_pass(request):
    """Create an access pass from a validated form."""
    form = AccessPassForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("dashboard")
    return render(request, "webapp/form.html", {"form": form, "title": "Новый пропуск"})


@login_required
def create_visit(request):
    """Create a visit and handle duplicate active records safely."""
    form = VisitForm(request.POST or None)
    if form.is_valid():
        visit = form.save(commit=False)
        visit.created_by = request.user
        try:
            visit.save()
        except IntegrityError:
            form.add_error(None, "У посетителя уже есть активное посещение на эту дату.")
        else:
            return redirect("dashboard")
    return render(request, "webapp/form.html", {"form": form, "title": "Новое посещение"})


@login_required
def cancel_visit(request, visit_id: int):
    """Cancel an existing visit using a POST request."""
    if request.method == "POST":
        visit = get_object_or_404(VisitRecord, pk=visit_id)
        visit.status = VisitRecord.Status.CANCELLED
        visit.save(update_fields=["status"])
    return redirect("dashboard")


@login_required
def visitors_api(request):
    """Return visitors as JSON for frontend integration."""
    visitors = VisitorRecord.objects.values("id", "full_name", "document")
    return JsonResponse({"results": list(visitors)})


@login_required
def visits_api(request):
    """Return visits as JSON for frontend integration."""
    visits = VisitRecord.objects.select_related("visitor", "employee")
    results = [
        {
            "id": visit.id,
            "visitor": visit.visitor.full_name,
            "employee": visit.employee.full_name,
            "date": visit.visit_date.isoformat(),
            "purpose": visit.purpose,
            "status": visit.status,
            "allowed": visit.is_allowed(),
        }
        for visit in visits
    ]
    return JsonResponse({"results": results})
