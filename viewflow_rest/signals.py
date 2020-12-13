#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2020-12-13 21:41:22


from django.dispatch import Signal


flow_started = Signal(providing_args=["process", "task"])
flow_finished = Signal(providing_args=["process", "task"])

task_started = Signal(providing_args=["process", "task"])
task_finished = Signal(providing_args=["process", "task"])
