"""Integration tests for the Django web interface."""

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import AccessPassRecord, EmployeeRecord, VisitorRecord, VisitRecord


class WebInterfaceTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester", password="StrongPass123!"
        )
        self.visitor = VisitorRecord.objects.create(
            full_name="Тестовый Посетитель", document="TEST-1"
        )
        self.employee = EmployeeRecord.objects.create(
            full_name="Тестовый Сотрудник", department="IT"
        )
        self.access_pass = AccessPassRecord.objects.create(
            number="TEST-PASS", visitor=self.visitor, expires_on=date.today() + timedelta(days=7)
        )

    def test_anonymous_user_is_redirected_and_does_not_see_logout(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 302)
        self.assertNotIn("Выйти", response.content.decode())

    def test_authenticated_dashboard_has_russian_actions(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Добавить посетителя")
        self.assertContains(response, "Добавить сотрудника")
        self.assertContains(response, "Выйти")

    def test_visit_form_rejects_pass_of_another_visitor(self):
        self.client.force_login(self.user)
        other = VisitorRecord.objects.create(full_name="Другой Посетитель", document="TEST-2")

        response = self.client.post(
            reverse("create_visit"),
            {
                "visitor": other.id,
                "employee": self.employee.id,
                "access_pass": self.access_pass.id,
                "visit_date": date.today().isoformat(),
                "purpose": "Проверка",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Выберите пропуск этого же посетителя")
        self.assertEqual(VisitRecord.objects.count(), 0)
