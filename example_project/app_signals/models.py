from django.db import models
from viewflow_rest.models import AbstractProcess, AbstractTask

# Create your models here.


class DeprecatedProcess(AbstractProcess):
    pass


class DeprecatedTask(AbstractTask):
    process = models.ForeignKey(
        DeprecatedProcess, on_delete=models.CASCADE)