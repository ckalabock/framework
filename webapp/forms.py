"""Forms used by the web interface."""

from django import forms

from .models import AccessPassRecord, EmployeeRecord, VisitRecord, VisitorRecord


class VisitorForm(forms.ModelForm):
    class Meta:
        model = VisitorRecord
        fields = ["full_name", "document"]


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeRecord
        fields = ["full_name", "department", "is_available"]


class AccessPassForm(forms.ModelForm):
    class Meta:
        model = AccessPassRecord
        fields = ["number", "visitor", "expires_on"]
        widgets = {"expires_on": forms.DateInput(attrs={"type": "date"})}


class VisitForm(forms.ModelForm):
    class Meta:
        model = VisitRecord
        fields = ["visitor", "employee", "access_pass", "visit_date", "purpose"]
        widgets = {"visit_date": forms.DateInput(attrs={"type": "date"})}
