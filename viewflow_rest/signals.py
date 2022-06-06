#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2020-12-13 21:41:22


from django.dispatch import Signal


flow_started = Signal()
flow_finished = Signal()

task_started = Signal()
task_finished = Signal()
