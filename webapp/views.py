"""Views backed by Django ORM models (Практика №9)."""

from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from .forms import VisitFilterForm, VisitForm
from .models import AccessPass, Employee, Visit, Visitor


def index(request):
    return render(request, "webapp/home.html", {
        "visitor_count": Visitor.objects.count(),
        "employee_count": Employee.objects.count(),
        "pass_count": AccessPass.objects.count(),
        "visit_count": Visit.objects.count(),
    })


def visitor_list(request):
    return render(request, "webapp/visitors/list.html", {"visitors": Visitor.objects.all()})


def visitor_detail(request, visitor_id):
    visitor = get_object_or_404(Visitor, pk=visitor_id)
    return render(request, "webapp/visitors/detail.html", {
        "visitor": visitor,
        "access_passes": visitor.access_passes.all(),
        "visits": visitor.visits.select_related("employee", "access_pass").all(),
    })


def employee_list(request):
    return render(request, "webapp/employees/list.html", {"employees": Employee.objects.all()})


def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    visits = employee.visits.select_related("visitor", "access_pass").all()
    return render(request, "webapp/employees/detail.html", {"employee": employee, "visits": visits})


def pass_list(request):
    access_passes = AccessPass.objects.select_related("visitor").all()
    return render(request, "webapp/passes/list.html", {"access_passes": access_passes})


def visit_list(request):
    visits = Visit.objects.select_related("visitor", "employee", "access_pass").all()
    form = VisitFilterForm(request.GET or None)
    if form.is_valid():
        data = form.cleaned_data
        if data["visit_date"]:
            visits = visits.filter(visit_date=data["visit_date"])
        if data["visitor"]:
            visits = visits.filter(visitor=data["visitor"])
        if data["employee"]:
            visits = visits.filter(employee=data["employee"])
        if data["status"]:
            visits = visits.filter(status=data["status"])
    return render(request, "webapp/visits/list.html", {"visits": visits, "form": form})


def visit_detail(request, visit_id):
    visit = get_object_or_404(Visit.objects.select_related("visitor", "employee", "access_pass"), pk=visit_id)
    return render(request, "webapp/visits/detail.html", {"visit": visit})


def visit_create(request):
    form = VisitForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        visit = form.save()
        return redirect("webapp:visit_detail", visit_id=visit.pk)
    return render(request, "webapp/visits/form.html", {"form": form, "title": "Новое посещение"})


def visit_edit(request, visit_id):
    visit = get_object_or_404(Visit, pk=visit_id)
    form = VisitForm(request.POST or None, instance=visit)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("webapp:visit_detail", visit_id=visit.pk)
    return render(request, "webapp/visits/form.html", {"form": form, "title": "Редактирование посещения"})


def visit_cancel(request, visit_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    visit = get_object_or_404(Visit, pk=visit_id)
    visit.status = Visit.Status.CANCELLED
    visit.save(update_fields=["status"])
    return redirect("webapp:visit_detail", visit_id=visit.pk)
