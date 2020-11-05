from django.contrib import admin

# Register your models here.

from . import models


@admin.register(models.HireProcess)
class HireProcessAdmin(models.ModelAdmin):
    pass
