from django.contrib import admin

# Register your models here.
# attendance/admin.py

from django.contrib import admin
from .models import Organisation, Visitor

admin.site.register(Organisation)
admin.site.register(Visitor)
