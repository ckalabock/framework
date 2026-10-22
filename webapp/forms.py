"""Forms used by the web interface."""

from django import forms

from .models import AccessPassRecord, EmployeeRecord, VisitRecord, VisitorRecord


class VisitorForm(forms.ModelForm):
    full_name = forms.CharField(label="ФИО посетителя")
    document = forms.CharField(label="Документ посетителя")

    class Meta:
        model = VisitorRecord
        fields = ["full_name", "document"]


class EmployeeForm(forms.ModelForm):
    full_name = forms.CharField(label="ФИО сотрудника")
    department = forms.CharField(label="Отдел")
    is_available = forms.BooleanField(label="Сотрудник доступен", required=False)

    class Meta:
        model = EmployeeRecord
        fields = ["full_name", "department", "is_available"]


class AccessPassForm(forms.ModelForm):
    number = forms.CharField(label="Номер пропуска")
    visitor = forms.ModelChoiceField(label="Посетитель", queryset=VisitorRecord.objects.all())
    expires_on = forms.DateField(
        label="Действует до",
        input_formats=["%Y-%m-%d", "%d.%m.%Y"],
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = AccessPassRecord
        fields = ["number", "visitor", "expires_on"]
        widgets = {"expires_on": forms.DateInput(attrs={"type": "date"})}


class VisitForm(forms.ModelForm):
    visitor = forms.ModelChoiceField(label="Посетитель", queryset=VisitorRecord.objects.all())
    employee = forms.ModelChoiceField(label="Принимающий сотрудник", queryset=EmployeeRecord.objects.all())
    access_pass = forms.ModelChoiceField(label="Пропуск", queryset=AccessPassRecord.objects.select_related("visitor"))
    visit_date = forms.DateField(
        label="Дата посещения",
        input_formats=["%Y-%m-%d", "%d.%m.%Y"],
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    purpose = forms.CharField(label="Цель посещения")

    def clean(self):
        cleaned_data = super().clean()
        visitor = cleaned_data.get("visitor")
        access_pass = cleaned_data.get("access_pass")
        if visitor and access_pass and access_pass.visitor_id != visitor.id:
            self.add_error("access_pass", "Выберите пропуск этого же посетителя.")
        return cleaned_data

    class Meta:
        model = VisitRecord
        fields = ["visitor", "employee", "access_pass", "visit_date", "purpose"]
        widgets = {"visit_date": forms.DateInput(attrs={"type": "date"})}
