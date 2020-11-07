#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2020-11-06 00:01:40

from django.utils.timezone import now
from .edges import STATUS_CHOICE
import logging


log = logging.getLogger(__name__)


class Activation(object):
    """
    flow_class, Flow类
    flow_class, Node实例
    task: 任务实例
    process: 进程实例
    """

    def __init__(self, *args, **kwargs):
        self.flow_class, self.flow_task = None, None
        self.process, self.task = None, None

    def prepare(self):
        pass

    def initialize(self, flow_task, task):
        log.info("初始化activation")
        self.flow_task, self.flow_class = flow_task, flow_task.flow_class
        self.process = self.flow_class.process_class._default_manager.get(
            flow_class=self.flow_class,
            pk=task.process_id)
        self.task = task

    def activate_next(self):
        if self.flow_task._next:
            self.flow_task._next.activate(
                prev_activation=self)


class StartActivation(Activation):

    def initialize(self, flow_task):
        self.flow_task, self.flow_class = flow_task, flow_task.flow_class
        self.process = self.flow_class.process_class(flow_class=self.flow_class)
        self.task = self.flow_class.task_class(flow_task=self.flow_task)

    def prepare(self):
        self.task.start_datetime = now()

    def done(self):
        self.process.save()
        self.task.process = self.process
        self.task.finish_datetime = now()
        self.task.status = STATUS_CHOICE.DONE
        self.task.save()
        log.info("StartActivation结束了")
        self.activate_next()
        log.info("下一个步骤激活了")

    def activate_next(self):
        if self.flow_task._next:
            self.flow_task._next.activate(
                prev_activation=self)


class EndActivation(Activation):

    def done(self):
        self.process.status = STATUS_CHOICE.DONE
        self.process.finish_datetime = now()
        self.process.save()
        self.task.finish_datetime = now()
        self.task.status = STATUS_CHOICE.DONE
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


class ViewActivation(Activation):

    @classmethod
    def create_task(cls, flow_task, prev_activation):
        return flow_task.flow_class.task_class(
            process=prev_activation.process,
            flow_task=flow_task,
        )

    @classmethod
    def activate(cls, flow_task, prev_activation):
        """
        本activation激活
        执行时间: 上一个node done的时候，触发下一个node的activate

        """
        task = cls.create_task(flow_task, prev_activation)

        task.status = STATUS_CHOICE.STARTED
        task.save()
        task.previous.add(prev_activation.task)

        activation = cls()
        activation.initialize(flow_task, task)

        return activation

    def done(self):
        log.info("ViewActivation结束")
        self.task.finish_datetime = now()
        self.task.status = STATUS_CHOICE.DONE
        self.task.save()

        self.activate_next()

    def activate_next(self):
        log.info("ViewActivation激活下一个")
        if self.flow_task._next:
            self.flow_task._next.activate(
                prev_activation=self)


class IfActivation(Activation):

    def __init__(self, **kwargs):
        self.condition_result = None

    def calculate_next(self):
        self.condition_result = self.flow_task.condition(self)

    def activate_next(self):
        if self.condition_result:
            self.flow_task._on_true.activate(prev_activation=self)
        else:
            self.flow_task._on_false.activate(prev_activation=self)

    def perform(self):
        self.task.start_datetime = now()
        self.task.save()

        self.calculate_next()

        self.task.finish_datetime = now()
        self.task.status = STATUS_CHOICE.DONE
        self.task.save()
        self.activate_next()

    @classmethod
    def activate(cls, flow_task, prev_activation):
        task = cls.create_task(flow_task, prev_activation)
        task.status = STATUS_CHOICE.STARTED
        task.save()
        task.previous.add(prev_activation.task)
        activation = cls()
        activation.initialize(flow_task, task)
        activation.perform()
        return activation

    @classmethod
    def create_task(cls, flow_task, prev_activation):
        return flow_task.flow_class.task_class(
            process=prev_activation.process,
            flow_task=flow_task,
        )
