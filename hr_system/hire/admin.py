from django.contrib import admin

# Register your models here.

from . import models


@admin.register(models.HireProcess)
class HireProcessAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "approved", "status", "create_datetime", "finish_datetime"]


@admin.register(models.HireTask)
class HireTask(admin.ModelAdmin):
    list_display = ["id", "flow_task", "flow_task_type", "status", "create_datetime", "finish_datetime", "operator"]
