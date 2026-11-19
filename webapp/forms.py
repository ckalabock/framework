"""Django forms for filtering and editing visits (ПР11)."""

from datetime import date

from django import forms
from django.core.exceptions import ValidationError

from .models import Employee, Visit, Visitor


class VisitFilterForm(forms.Form):
    visit_date = forms.DateField(
        label="Дата посещения", required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    visitor = forms.ModelChoiceField(
        label="Посетитель", queryset=Visitor.objects.all(), required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    employee = forms.ModelChoiceField(
        label="Сотрудник", queryset=Employee.objects.all(), required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    status = forms.ChoiceField(
        label="Статус", choices=(("", "Все статусы"), *Visit.Status.choices),
        required=False, widget=forms.Select(attrs={"class": "form-select"}),
    )


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ("visitor", "employee", "access_pass", "visit_date", "purpose", "status")
        labels = {"access_pass": "Пропуск", "visit_date": "Дата посещения"}
        widgets = {
            "visitor": forms.Select(attrs={"class": "form-select"}),
            "employee": forms.Select(attrs={"class": "form-select"}),
            "access_pass": forms.Select(attrs={"class": "form-select"}),
            "visit_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "purpose": forms.TextInput(attrs={"class": "form-control", "placeholder": "Укажите цель посещения"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_visit_date(self):
        visit_date = self.cleaned_data["visit_date"]
        if visit_date < date.today():
            raise ValidationError("Дата посещения не может быть в прошлом.")
        return visit_date

    def clean(self):
        cleaned_data = super().clean()
        visitor = cleaned_data.get("visitor")
        employee = cleaned_data.get("employee")
        access_pass = cleaned_data.get("access_pass")
        visit_date = cleaned_data.get("visit_date")
        status = cleaned_data.get("status")
        if not all((visitor, employee, access_pass, visit_date)):
            return cleaned_data
        if access_pass.visitor_id != visitor.pk:
            self.add_error("access_pass", "Выбранный пропуск принадлежит другому посетителю.")
        if access_pass.expires_on < visit_date:
            self.add_error("access_pass", "Срок действия пропуска истекает до даты посещения.")
        if not employee.is_available and status == Visit.Status.ACTIVE:
            self.add_error("employee", "Сотрудник сейчас недоступен для приёма посетителей.")
        conflicts = Visit.objects.filter(
            employee=employee, visit_date=visit_date, status=Visit.Status.ACTIVE
        )
        if self.instance.pk:
            conflicts = conflicts.exclude(pk=self.instance.pk)
        if status == Visit.Status.ACTIVE and conflicts.exists():
            raise ValidationError("У сотрудника уже есть активное посещение на выбранную дату.")
        return cleaned_data
