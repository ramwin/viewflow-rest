from django.db import models
from viewflow_rest.models import AbstractProcess, AbstractTask
from rest_framework.generics import RetrieveUpdateAPIView

# Create your models here.


class HireProcess(AbstractProcess):
    GENDER_CHOICES = (
        ("男", "男"),
        ("女", "女"),
    )
    name = models.CharField("候选人姓名", max_length=31)
    gender = models.CharField("候选人性别", choices=GENDER_CHOICES, max_length=1)
    approved = models.BooleanField(null=True, blank=True)
    salary = models.DecimalField(
        "每月薪资",
        max_digits=9,
        decimal_places=2,
        null=True, blank=True)
    notified = models.BooleanField("是否已经发送offer通知", blank=True, default=False)
    background_ok = models.BooleanField("背景调查是否通过", blank=True, null=True)

    class Meta:
        verbose_name = verbose_name_plural = "招聘流程"


class HireTask(AbstractTask):
    process = models.ForeignKey(
        HireProcess, related_name="tasks", on_delete=models.CASCADE)

    class Meta:
        verbose_name = verbose_name_plural = "招聘任务"
