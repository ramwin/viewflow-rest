#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2020-11-05 22:02:09


import logging
from django.urls import path, include

from . import flows


log = logging.getLogger(__name__)


log.info("执行hire.urls.py")

flow = flows.HireFlow()

urls = flow.urls
log.info("执行完毕")
log.info(f"urls: {urls}")


app_name = "hire"

urlpatterns = [
    path("hireflow/", include((urls, "hireflow"), namespace="hireflow")),
]
