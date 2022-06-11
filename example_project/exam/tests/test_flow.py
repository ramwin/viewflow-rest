#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


from django.test import TestCase

from viewflow_rest.edges import STATUS_CHOICE
from exam import flows
from exam.models import ExamProcess


class FlowTest(TestCase):

    def test(self):
        activation = flows.exam_flow.register.activation_class()
        flow_task = flows.exam_flow.register
        activation.initialize(flow_task, task=None)
        activation.done(operator=None)
        self.exam_process = ExamProcess.objects.get()
        self.assertEqual(
            ExamProcess.objects.count(),
            1
        )
        self.assertEqual(
            self.exam_process.tasks.count(),
            2
        )
        self.assertEqual(
            self.exam_process.tasks.get(flow_task="register").status,
            STATUS_CHOICE.DONE,
        )
        self.assertEqual(
            self.exam_process.tasks.get(flow_task="select_term").status,
            STATUS_CHOICE.STARTED,
        )
