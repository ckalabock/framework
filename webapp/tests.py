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

    def test_get_filter_form_filters_visits(self):
        response = self.client.get(reverse("webapp:visit_list"), {"status": Visit.Status.ACTIVE})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["visits"]), 1)

    def test_visit_form_rejects_expired_pass(self):
        visitor = Visitor.objects.first()
        employee = Employee.objects.first()
        expired = AccessPass.objects.create(number="OLD", visitor=visitor, expires_on=date(2028, 1, 1))
        response = self.client.post(reverse("webapp:visit_create"), {
            "visitor": visitor.pk, "employee": employee.pk, "access_pass": expired.pk,
            "visit_date": "2029-01-02", "purpose": "Проверка", "status": Visit.Status.ACTIVE,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Срок действия пропуска")

    def test_cancel_visit_uses_post_and_changes_status(self):
        visit = Visit.objects.first()
        response = self.client.post(reverse("webapp:visit_cancel", args=[visit.pk]))
        self.assertRedirects(response, reverse("webapp:visit_detail", args=[visit.pk]))
        visit.refresh_from_db()
        self.assertEqual(visit.status, Visit.Status.CANCELLED)
