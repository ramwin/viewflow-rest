from django.contrib import admin

# Register your models here.

from . import models


@admin.register(models.HireProcess)
class HireProcessAdmin(admin.ModelAdmin):
    pass


@admin.register(models.HireTask)
class HireTask(admin.ModelAdmin):
    pass
