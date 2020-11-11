#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2020-11-05 19:51:05

import logging

from . import edges, activations, mixins
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
        log.debug(f"我{self}准备好了")
        pass

    def urls(self):
        return []

    def _resolve(self, resolver):
        if self._next:
            self._next = resolver.get_implementation(self._next)

    def activate(self, prev_activation):
        self.activation_class.activate(self, prev_activation)

    def _incoming(self):
        return self._incoming_edges

    def can_execute(self, user, task=None):
        return True


class If(Node):

    task_type = "IF"
    activation_class = activations.IfActivation

    def __init__(self, cond, **kwargs):
        super().__init__(**kwargs)
        self._condtion = cond
        self._on_true = None
        self._on_false = None

    def Then(self, node):
        self._on_true = node
        return self

    def Else(self, node):
        self._on_false = node
        return self

    @property
    def condition(self):
        return self._condtion

    def _outgoing(self):
        return [
            edges.Edge(src=self, dst=self._on_true, edge_class="cond_true"),
            edges.Edge(src=self, dst=self._on_false, edge_class="cond_false"),
        ]

    def activate(self, prev_activation):
        self.activation_class.activate(self, prev_activation)

    def _resolve(self, resolver):
        self._on_true = resolver.get_implementation(self._on_true)
        self._on_false = resolver.get_implementation(self._on_false)


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


class Start(mixins.PermissionMixin, NextNodeMixin, Node, ViewArgsMixin):

    task_type = "START"
    activation_class = activations.StartActivation

    def __init__(self, viewclass=None, *args, **kwargs):
        log.debug("Start.init")
        log.debug(args)
        log.debug(kwargs)
        self._view = viewclass
        if viewclass is None:
            raise Exception("不对")
        super().__init__(viewclass, **kwargs)

    @property
    def view(self):
        log.debug("根据参数生成view")
        return self._view(**self._view_args)

    def urls(self):
        log.debug("返回Start.urls")
        urls = super().urls()
        url = path('start/', self.view.as_view(), {'flow_task': self}, name="start")
        urls.append(url)
        return urls

    def can_execute(self, user, task=None):
        if self._owner_group:
            return user in self._owner_group.user_set.all()
        return True


class End(Node):
    activation_class = activations.EndActivation

    task_type = "END"

    def _outgoing(self):
        return []


class View(mixins.PermissionMixin, NextNodeMixin, Node, ViewArgsMixin):

    activation_class = activations.ViewActivation

    task_type = "HUMAN"

    def __init__(self, viewclass=None, *args, **kwargs):
        log.debug("初始化View")
        self._view = viewclass
        super().__init__(viewclass, **kwargs)

    def urls(self):
        urls = super().urls()
        urls.append(
            path(
                f"<slug:process_id>/{self.name}/<slug:task_id>/",
                self.view.as_view(), {'flow_task': self}, name=self.name
            )
        )
        log.debug(f"返回View.urls: {urls}")
        return urls

    @property
    def view(self):
        return self._view(**self._view_args)

    def can_execute(self, user, task):
        if self._owner_group:
            return user in self._owner_group.user_set.all()
        return True


class Split(Node, ViewArgsMixin):
    task_type = "SPLIT"
    activation_class = activations.SplitActivation

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._activate_next = []

    def _outgoing(self):
        for next_node, cond in self._activate_next:
            edge_class = "cond_true" if cond else "default"
            yield edges.Edge(src=self, dst=next_node, edge_class=edge_class)

    def _resolve(self, resolver):
        self._activate_next = \
            [(resolver.get_implementation(node), cond)
                for node, cond in self._activate_next]

    def Next(self, node, cond=None):
        self._activate_next.append((node, cond))
        return self

    def Always(self, node):
        return self.Next(node)


class Join(NextNodeMixin, Node, ViewArgsMixin):
    task_type = "JOIN"
    activation_class = activations.JoinActivation
