#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2020-11-05 21:17:16


from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from . import fields
from .edges import STATUS_CHOICE



class AbstractProcess(models.Model):
    flow_class = fields.FlowReferenceField('Flow')
    status = models.CharField("状态", choices=STATUS_CHOICE.choices, max_length=15, default=STATUS_CHOICE.STARTED)
    create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)
    finish_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class AbstractTask(models.Model):
    """
    A task should not be assigned, if you need to assign a task, you can add a node which do the thing
    """
    flow_task = fields.TaskReferenceField('Task')
    flow_task_type = models.CharField("类型", max_length=31)
    status = models.CharField("状态", choices=STATUS_CHOICE.choices, max_length=15)
    create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)
    finish_datetime = models.DateTimeField(blank=True, null=True)
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    previous = models.ManyToManyField(
        'self', symmetrical=False, related_name='leading',
        verbose_name="上级任务")

    class Meta:
        abstract = True
