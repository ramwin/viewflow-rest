#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2020-11-05 19:51:05

import logging

from . import edges, activations
from django.urls import path, re_path
from django.views.generic.base import RedirectView


log = logging.getLogger(__name__)


class Node(object):

    def __init__(self, activation_class=None, *args, **kwargs):
        self._incoming_edges = []
        self._next = None
        super().__init__(*args, **kwargs)

    def Next(self, node):
        self._next = node
        return self

    def ready(self):
        log.info(f"我{self}准备好了")
        pass

    def urls(self):
        return []

    def _resolve(self, resolver):
        if self._next:
            self._next = resolver.get_implementation(self._next)

    def activate(self, prev_activation):
        self.activation_class.activate(self, prev_activation)


class If(Node):

    def __init__(self, condition):
        super().__init__(condition)
        self._condtion = condition
        self._on_true = None
        self._on_false = None

    def Then(self, node):
        self._on_true = node

    def Else(self, node):
        self._on_false = node

    @property
    def condition(self):
        return self._condtion


class End(Node):

    task_type = "END"


class Task(Node):
    pass


class ViewArgsMixin(object):

    def __init__(self, **kwargs):
        self._view_args = kwargs


class NextNodeMixin(object):

    def _outgoing(self):
        if self._next:
            return [
                edges.Edge(src=self, dst=self._next, edge_class='next')
            ]
        return []


class Start(NextNodeMixin, Node, ViewArgsMixin):

    task_type = "START"
    activation_class = activations.StartActivation

    def __init__(self, viewclass=None, *args, **kwargs):
        log.info("Start.init")
        log.info(args)
        log.info(kwargs)
        self._view = viewclass
        if viewclass is None:
            raise Exception("不对")
        super().__init__(viewclass, **kwargs)

    @property
    def view(self):
        log.info("根据参数生成view")
        return self._view(**self._view_args)

    def urls(self):
        log.info("返回Start.urls")
        urls = super().urls()
        url = path('start/', self.view.as_view(), {'flow_task': self}, name="start")
        urls.append(url)
        return urls


class End(Node):
    activation_class = activations.EndActivation

    task_type = "END"

    def _outgoing(self):
        return []


class View(NextNodeMixin, Node, ViewArgsMixin):

    activation_class = activations.ViewActivation

    task_type = "HUMAN"

    def __init__(self, viewclass=None, *args, **kwargs):
        log.info("初始化View")
        self._view = viewclass
        super().__init__(viewclass, **kwargs)

    def urls(self):
        urls = super().urls()
        urls.append(
            path(
                f"<int:process_id>/{self.name}/<int:task_id>/",
                self.view.as_view(), {'flow_task': self}, name=self.name
            )
        )
        log.info(f"返回View.urls: {urls}")
        return urls

    @property
    def view(self):
        return self._view(**self._view_args)
