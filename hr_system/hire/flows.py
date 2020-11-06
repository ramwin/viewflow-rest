#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2020-11-05 21:15:52


import logging

from viewflow_rest import flows, nodes, views, rest_extensions, this

from . import models


log = logging.getLogger(__name__)
log.info("引入hire.flows.py")



class HireFlow(flows.Flow):

    process_class = models.HireProcess
    task_class = models.HireTask

    start = nodes.Start(
        viewclass=rest_extensions.AutoCreateAPIView,
        fields=["id", "name", "gender"],
    ).Next(
        this.approve
    )

    approve = nodes.View(
        viewclass=rest_extensions.AutoUpdateAPIView,
        fields=["approved"],
    ).Next(
        this.end
    )

    end = nodes.End()


log.info("引入hire.flows.py结束")
log.info(HireFlow._meta.nodes())
