#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import logging

from viewflow_rest import flows, nodes, rest_extensions, this
from viewflow_rest.signals import task_finished

from . import models, serializers


logger = logging.getLogger(__name__)


class ExamFlow(flows.Flow):

    process_class = models.ExamProcess
    task_class = models.ExamTask

    register = nodes.Start(
        viewclass=rest_extensions.AutoCreateAPIView,
        serializer_class=serializers.RegisterExamSerializer,
    ).Next(
        this.select_term
    )

    select_term = nodes.View(
        viewclass=rest_extensions.AutoUpdateAPIView,
        fields=["term"],
    ).Next(this.take_exam)

    take_exam = nodes.View(
        viewclass=rest_extensions.AutoUpdateAPIView,
        fields=["grade"],
    ).Next(this.check_grade)

    check_grade = nodes.If(
        cond=lambda activation: activation.process.passed
    ).Then(this.end).Else(this.select_term)
    end = nodes.End()


exam_flow = ExamFlow()


task_finished.connect(
    models.ExamProcess.update_pass,
    sender=ExamFlow.take_exam,
)
