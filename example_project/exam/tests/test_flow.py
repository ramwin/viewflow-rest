#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>

import pendulum

from django.test import TestCase

from viewflow_rest.edges import STATUS_CHOICE
from exam import flows
from exam.models import ExamProcess, ExamTask


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
        # first round
        select_term = self.exam_process.tasks.get(
            flow_task="select_term")
        select_term.term = pendulum.yesterday().date()
        select_term.save()
        select_term.auto_finish()
        self.assertEqual(
            select_term.status,
            STATUS_CHOICE.DONE,
        )
        take_exam = select_term.leading.get()
        self.assertEqual(
            take_exam.flow_task,
            "take_exam",
        )
        take_exam.grade = 50  # failed
        take_exam.save()
        take_exam.auto_finish()
        self.assertEqual(
            self.exam_process.tasks.filter(flow_task="select_term").count(),
            2,
        )
        self.assertEqual(
            take_exam.leading.get().leading.get().flow_task,
            "select_term",
        )
        ExamTask.objects.order_by("id").last().auto_finish()
        take_exam = ExamTask.objects.order_by("id").last()
        take_exam.grade = 60
        take_exam.save()
        take_exam.auto_finish()
        self.assertEqual(
            self.exam_process.tasks.filter(flow_task="select_term").count(),
            2,
        )
        self.assertTrue(
            self.exam_process.tasks.filter(flow_task="end").exists()
        )
        end_task = self.exam_process.tasks.get(flow_task="end")
        end_task.auto_finish()
        self.exam_process.refresh_from_db()
        self.assertEqual(
            self.exam_process.status,
            STATUS_CHOICE.DONE,
        )
