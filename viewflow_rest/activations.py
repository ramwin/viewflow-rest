#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2020-11-06 00:01:40

from django.utils.timezone import now
from .edges import STATUS_CHOICE
import logging


log = logging.getLogger(__name__)


class Activation(object):

    def __init__(self, *args, **kwargs):
        self.flow_class, self.flow_task = None, None
        self.process, self.task = None, None

    def prepare(self):
        pass

    @classmethod
    def activate(cls, flow_task):
        log.info(f"我被激活了: {flow_task}")


class StartActivation(Activation):

    def initializer(self, flow_task):
        self.flow_task, self.flow_class = flow_task, flow_task.flow_class
        self.process = self.flow_class.process_class(flow_class=self.flow_class)
        self.task = self.flow_class.task_class(flow_task=self.flow_task)

    def prepare(self):
        self.task.start_datetime = now()

    def done(self):
        self.process.save()
        self.task.process = self.process
        self.task.finished = now()
        self.task.save()
        self.activate_next()

    def activate_next(self):
        if self.flow_task._next:
            self.flow_task._next.activate(
                prev_activation=self)


class EndActivation(Activation):

    def initializer(self, flow_task, task):

        pass

    def done(self):
        self.process.status = STATUS_CHOICE.DONE
        self.process.finished_datetime = now()
        self.process.save()
        self.task.finished_datetime = now()
        self.task.save()

    @classmethod
    def activate(cls, flow_task, prev_activation):
        flow_class, flow_task = flow_task.flow_class, flow_task
        process = prev_activation.process
        task = flow_class.task_class(
            process=process,
            flow_task=flow_task,
        )
        task.save()
        task.previous.add(prev_activation.task)

        activation = cls()
        activation.initialize(flow_task, task)
        activation.done()
        return activation
