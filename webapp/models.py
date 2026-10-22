"""Database models for the visitor accounting web application."""

from django.conf import settings
from django.db import models


class VisitorRecord(models.Model):
    """A visitor and their identity document."""

    full_name = models.CharField(max_length=150)
    document = models.CharField(max_length=40, unique=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self) -> str:
        return self.full_name


class EmployeeRecord(models.Model):
    """An employee who can receive visitors."""

    full_name = models.CharField(max_length=150)
    department = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self) -> str:
        return f"{self.full_name} ({self.department})"


class AccessPassRecord(models.Model):
    """A visitor access pass."""

    number = models.CharField(max_length=40, unique=True)
    visitor = models.ForeignKey(VisitorRecord, on_delete=models.CASCADE, related_name="passes")
    expires_on = models.DateField()

    def __str__(self) -> str:
        return self.number


class VisitRecord(models.Model):
    """A planned or completed visit."""

    class Status(models.TextChoices):
        ACTIVE = "active", "Активно"
        CANCELLED = "cancelled", "Отменено"

    visitor = models.ForeignKey(VisitorRecord, on_delete=models.PROTECT, related_name="visits")
    employee = models.ForeignKey(EmployeeRecord, on_delete=models.PROTECT, related_name="visits")
    access_pass = models.ForeignKey(AccessPassRecord, on_delete=models.PROTECT, related_name="visits")
    visit_date = models.DateField()
    purpose = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["visitor", "visit_date"],
                condition=models.Q(status="active"),
                name="unique_active_visitor_date",
            )
        ]
        ordering = ["-visit_date", "-created_at"]

    def is_allowed(self) -> bool:
        """Check business rules for access."""
        from django.utils import timezone

        return (
            self.status == self.Status.ACTIVE
            and self.access_pass.expires_on >= self.visit_date
            and self.employee.is_available
            and self.visit_date >= timezone.localdate()
        )

    def __str__(self) -> str:
        state = "допуск разрешён" if self.is_allowed() else "допуск запрещён"
        return f"{self.visitor} — {self.visit_date:%d.%m.%Y}: {state}"
