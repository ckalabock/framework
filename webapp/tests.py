"""HTTP and ORM tests for the visitor accounting application."""

from datetime import date

from django.test import TestCase
from django.urls import reverse

from .models import AccessPass, Employee, Visit, Visitor


class WebPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        visitor = Visitor.objects.create(full_name="Тестовый посетитель", document="T-1")
        employee = Employee.objects.create(full_name="Тестовый сотрудник", department="ИТ")
        access_pass = AccessPass.objects.create(number="TEST-1", visitor=visitor, expires_on=date(2030, 1, 1))
        Visit.objects.create(visitor=visitor, employee=employee, access_pass=access_pass, visit_date=date(2029, 1, 1), purpose="Проверка")

    def test_home_page_uses_orm_counts(self):
        response = self.client.get(reverse("webapp:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Система учёта посетителей")

    def test_related_objects_are_available(self):
        visitor = Visitor.objects.get(full_name="Тестовый посетитель")
        self.assertEqual(visitor.access_passes.count(), 1)
        self.assertEqual(visitor.visits.first().employee.full_name, "Тестовый сотрудник")

    def test_dynamic_pages_and_404(self):
        visitor = Visitor.objects.first()
        self.assertEqual(self.client.get(reverse("webapp:visitor_detail", args=[visitor.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse("webapp:visit_detail", args=[999999])).status_code, 404)
