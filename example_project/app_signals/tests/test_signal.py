#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import pendulum

from django.test import TestCase

from viewflow_rest.edges import STATUS_CHOICE
from app_signals import flows
# from app_signals.models import ExamProcess, ExamTask


class SignalTest(TestCase):

    def test(self):
        with self.assertRaises(DeprecationWarning):
            activation = flows.deprecated_flow.start.activation_class()
            flow_task = flows.deprecated_flow.start
            activation.initialize(flow_task, task=None)
            activation.done(operator=None)
