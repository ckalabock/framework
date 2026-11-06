"""Load the demonstration JSON records into the Django ORM database."""

from django.core.management.base import BaseCommand

from storage import load_access_passes, load_employees, load_visitors, load_visits
from webapp.models import AccessPass, Employee, Visit, Visitor


class Command(BaseCommand):
    help = "Перенести демонстрационные записи из data/*.json в SQLite через ORM"

    def handle(self, *args, **options):
        old_visitors = load_visitors()
        old_employees = load_employees()
        old_passes = load_access_passes(old_visitors)
        old_visits = load_visits(old_visitors, old_employees, old_passes)

        Visit.objects.all().delete()
        AccessPass.objects.all().delete()
        Employee.objects.all().delete()
        Visitor.objects.all().delete()

        visitors = {
            item.visitor_id: Visitor.objects.create(
                id=item.visitor_id, full_name=item.full_name, document=item.document
            )
            for item in old_visitors
        }
        employees = {
            item.employee_id: Employee.objects.create(
                id=item.employee_id,
                full_name=item.full_name,
                department=item.department,
                is_available=item.is_available,
            )
            for item in old_employees
        }
        passes = {
            item.pass_id: AccessPass.objects.create(
                id=item.pass_id,
                number=item.number,
                visitor=visitors[item.visitor.visitor_id],
                expires_on=item.expires_on,
            )
            for item in old_passes
        }
        for item in old_visits:
            Visit.objects.create(
                id=item.visit_id,
                visitor=visitors[item.visitor.visitor_id],
                employee=employees[item.employee.employee_id],
                access_pass=passes[item.access_pass.pass_id],
                visit_date=item.visit_date,
                purpose=item.purpose,
                status=item.status,
            )

        self.stdout.write(self.style.SUCCESS(
            f"Перенесено: посетителей {len(visitors)}, сотрудников {len(employees)}, "
            f"пропусков {len(passes)}, посещений {len(old_visits)}."
        ))
