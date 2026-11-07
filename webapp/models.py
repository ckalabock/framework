"""Django ORM models for the visitor accounting domain (Практика №9)."""

from django.db import models


class Visitor(models.Model):
    full_name = models.CharField("полное имя", max_length=200)
    document = models.CharField("документ", max_length=80, blank=True, default="")

    class Meta:
        ordering = ["full_name"]
        verbose_name = "посетитель"
        verbose_name_plural = "посетители"

    def __str__(self):
        return self.full_name


class Employee(models.Model):
    full_name = models.CharField("полное имя", max_length=200)
    department = models.CharField("подразделение", max_length=120, blank=True, default="")
    is_available = models.BooleanField("доступен", default=True)

    class Meta:
        ordering = ["full_name"]
        verbose_name = "сотрудник"
        verbose_name_plural = "сотрудники"

    def __str__(self):
        return self.full_name


class AccessPass(models.Model):
    number = models.CharField("номер пропуска", max_length=30, unique=True)
    visitor = models.ForeignKey(Visitor, on_delete=models.PROTECT, related_name="access_passes", verbose_name="посетитель")
    expires_on = models.DateField("действует до")

    class Meta:
        ordering = ["number"]
        verbose_name = "пропуск"
        verbose_name_plural = "пропуска"

    def __str__(self):
        return f"{self.number} — {self.visitor.full_name}"


class Visit(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "активно", "Активно"
        CANCELLED = "отменено", "Отменено"

    visitor = models.ForeignKey(Visitor, on_delete=models.PROTECT, related_name="visits", verbose_name="посетитель")
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="visits", verbose_name="сотрудник")
    access_pass = models.ForeignKey(AccessPass, on_delete=models.PROTECT, related_name="visits", verbose_name="пропуск")
    visit_date = models.DateField("дата посещения")
    purpose = models.CharField("цель", max_length=300, blank=True, default="")
    status = models.CharField("статус", max_length=20, choices=Status.choices, default=Status.ACTIVE)

    class Meta:
        ordering = ["-visit_date", "-id"]
        verbose_name = "посещение"
        verbose_name_plural = "посещения"

    def __str__(self):
        return f"{self.visit_date:%d.%m.%Y}: {self.visitor} → {self.employee}"

    def is_allowed(self):
        return self.status == self.Status.ACTIVE and self.access_pass.expires_on >= self.visit_date and self.employee.is_available


# Соответствие учебному примеру Roomly из таблицы 7.3:
# Room → Visitor (объект, который бронируется/учитывается),
# User → Employee, Booking → Visit.
# Эти имена можно показать преподавателю при объяснении адаптации примера
# под предметную область учёта посетителей.
Room = Visitor
User = Employee
Booking = Visit
