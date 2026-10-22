"""Load safe demonstration data for local development."""

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from webapp.models import AccessPassRecord, EmployeeRecord, VisitRecord, VisitorRecord


class Command(BaseCommand):
    help = "Create demonstration visitors, employees, passes and visits."

    def handle(self, *args, **options):
        user_model = get_user_model()
        user, _ = user_model.objects.get_or_create(
            username="demo",
            defaults={"email": "demo@example.com", "is_staff": True},
        )
        user.set_password("DemoPass123!")
        user.save()

        visitor_1, _ = VisitorRecord.objects.get_or_create(
            document="DEMO-1001",
            defaults={"full_name": "Иванов Иван Иванович"},
        )
        visitor_2, _ = VisitorRecord.objects.get_or_create(
            document="DEMO-1002",
            defaults={"full_name": "Петрова Мария Сергеевна"},
        )
        employee_1, _ = EmployeeRecord.objects.get_or_create(
            full_name="Смирнов Алексей Олегович",
            defaults={"department": "Отдел кадров", "is_available": True},
        )
        employee_2, _ = EmployeeRecord.objects.get_or_create(
            full_name="Кузнецова Анна Викторовна",
            defaults={"department": "IT-отдел", "is_available": False},
        )
        pass_1, _ = AccessPassRecord.objects.get_or_create(
            number="DEMO-A-001",
            defaults={"visitor": visitor_1, "expires_on": date.today() + timedelta(days=90)},
        )
        pass_2, _ = AccessPassRecord.objects.get_or_create(
            number="DEMO-B-002",
            defaults={"visitor": visitor_2, "expires_on": date.today() - timedelta(days=1)},
        )
        VisitRecord.objects.get_or_create(
            visitor=visitor_1,
            visit_date=date.today(),
            defaults={
                "employee": employee_1,
                "access_pass": pass_1,
                "purpose": "Деловая встреча",
                "created_by": user,
                "status": VisitRecord.Status.ACTIVE,
            },
        )
        VisitRecord.objects.get_or_create(
            visitor=visitor_2,
            visit_date=date.today() - timedelta(days=1),
            defaults={
                "employee": employee_2,
                "access_pass": pass_2,
                "purpose": "Просроченный пропуск",
                "created_by": user,
                "status": VisitRecord.Status.CANCELLED,
            },
        )
        self.stdout.write(self.style.SUCCESS("Демо-данные добавлены. Логин: demo, пароль: DemoPass123!"))
