#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import pendulum

from django.test import TestCase

from viewflow_rest.edges import STATUS_CHOICE
from app_signals import flows, models
# from app_signals.models import ExamProcess, ExamTask


class SignalTest(TestCase):

    def test(self):
        activation = flows.deprecated_flow.start.activation_class()
        flow_task = flows.deprecated_flow.start
        activation.initialize(flow_task, task=None)
        activation.done(operator=None)

        # first warning
        models.DeprecatedTask.objects.last().auto_finish()

        # second error
        with self.assertRaises(DeprecationWarning):
            models.DeprecatedTask.objects.last().auto_finish()