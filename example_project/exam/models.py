from django.db import models

from viewflow_rest.models import AbstractProcess, AbstractTask

# Create your models here.


class ExamProcess(AbstractProcess):
    SUBJECT_CHOICES = (
        ("math", "math"),
        ("art", "art"),
    )
    subject = models.CharField("subject",
                               max_length=31,
                               choices=SUBJECT_CHOICES)
    passed = models.BooleanField(default=False)


class ExamTask(AbstractTask):

    process = models.ForeignKey(ExamProcess,
                                on_delete=models.CASCADE, related_name="tasks")
    term = models.DateField(null=True)
