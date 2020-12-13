#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2020-11-05 21:15:52


import logging

from viewflow_rest import flows, nodes, views, rest_extensions, this
from django.contrib.auth.models import Group
from viewflow_rest import signals

from . import models, serializers


log = logging.getLogger(__name__)
log.info("引入hire.flows.py")



class HireFlow(flows.Flow):

    process_class = models.HireProcess
    task_class = models.HireTask

    start = nodes.Start(
        viewclass=rest_extensions.AutoCreateAPIView,
        serializer_class=serializers.AddCandidateSerializer,
    ).Permission(
        group=Group.objects.get_or_create(name="hr")[0]
    ).Next(
        this.split_to_3rd_and_direct_leader
    )

    split_to_3rd_and_direct_leader = nodes.Split(
    ).Always(
        this.approve
    ).Always(
        this.background_research
    )

    background_research = nodes.View(
        viewclass=rest_extensions.AutoUpdateAPIView,
        fields=["background_ok"],
    ).Next(
        this.check_background
    )

    check_background = nodes.If(
        cond=lambda activation: activation.process.background_ok
    ).Then(
        this.join_on_both_approve
    ).Else(
        this.end
            )

    join_on_both_approve = nodes.Join().Next(
        this.notify
    )

    notify = nodes.View(
        viewclass=rest_extensions.AutoUpdateAPIView,
        fields=["notified"],
    ).Next(
        this.end
    )

    approve = nodes.View(
        viewclass=rest_extensions.AutoUpdateAPIView,
        serializer_class = serializers.ApproveSerializer,
        # fields=["approved"],
    ).Permission(
        group=Group.objects.get_or_create(name="leader")[0]
    ).Next(
        this.check_if_approve
    )

    check_if_approve = nodes.If(
        cond=lambda activation: activation.process.approved
    ).Then(
        this.set_salary
    ).Else(
        this.notify
    )

    set_salary = nodes.View(
        viewclass=rest_extensions.AutoUpdateAPIView,
        fields=["salary"],
    ).Permission(
        group=Group.objects.get_or_create(name="hr")[0]
    ).Next(
        this.join_on_both_approve
    )

    end = nodes.End()


log.info("引入hire.flows.py结束")
log.info(HireFlow._meta.nodes())


def task_started(**kwargs):
    log.info("任务开始了")
    log.info(kwargs["task"])

def task_finished(**kwargs):
    log.info("任务结束了")
    log.info(kwargs["task"])

def flow_started(**kwargs):
    log.info("流程开始了")
    log.info(kwargs)

def flow_finished(**kwargs):
    log.info("流程结束了")


signals.task_finished.connect(task_finished)
signals.task_started.connect(task_started)
signals.flow_started.connect(flow_started)
signals.flow_finished.connect(flow_finished)
