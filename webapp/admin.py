from django.contrib import admin

from .models import AccessPassRecord, EmployeeRecord, VisitRecord, VisitorRecord

admin.site.register([VisitorRecord, EmployeeRecord, AccessPassRecord, VisitRecord])
