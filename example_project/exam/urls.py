#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>

from django.urls import path, include

from . import flows


urlpatterns = [
    path("exam/",
         include(
             (flows.exam_flow.urls, "hireflow"),
             namespace="exam")),
]
