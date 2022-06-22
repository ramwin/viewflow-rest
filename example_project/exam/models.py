import logging

from django.db import models

from viewflow_rest.models import AbstractProcess, AbstractTask
from viewflow_rest.signals import task_finished


logger = logging.getLogger(__name__)


class ExamProcess(AbstractProcess):
    SUBJECT_CHOICES = (
        ("math", "math"),
        ("art", "art"),
    )
    subject = models.CharField("subject",
                               max_length=31,
                               choices=SUBJECT_CHOICES)
    passed = models.BooleanField(default=False)

    @classmethod
    def update_pass(cls, task, **kwargs):
        assert isinstance(task, ExamTask)
        logger.info("calling ExamProcess.update_pass")
        if task.flow_task == "take_exam":
            logger.info(f"the student has taken the exam, score is {task.grade}")
            task.process.passed = task.grade >= 60
            logger.info(f"the student passed the exam? : {task.process.passed}")
            task.process.save()


class ExamTask(AbstractTask):

    process = models.ForeignKey(ExamProcess,
                                on_delete=models.CASCADE, related_name="tasks")
    grade = models.IntegerField(default=0)
    term = models.DateField(null=True)
