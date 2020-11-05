#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2020-11-05 21:17:16


from django.db import models
from django.db.models import TextChoices
from . import fields


class STATUS_CHOICE(TextChoices):
    NEW = "NEW", "创建了"
    STARTED = "STARTED", "开始了"
    DONE = "DONE", "结束了"
    CANCELED = "CANCELED", "取消了"


class AbstractProcess(models.Model):
    flow_class = fields.FlowReferenceField('Flow', max_length=63)
    status = models.CharField("状态", choices=STATUS_CHOICE.choices, max_length=15)
    create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)
    finished_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class AbstractTask(models.Model):
    flow_task = fields.TaskReferenceField('Task', max_length=63)
    flow_task_type = models.CharField("类型", max_length=31)
    status = models.CharField("状态", choices=STATUS_CHOICE.choices, max_length=15)
    create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)
    finished_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True
