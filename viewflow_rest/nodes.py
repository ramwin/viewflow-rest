#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2020-11-05 19:51:05

import logging


log = logging.getLogger(__name__)


class Node(object):

    def __init__(self, activation_class=None, *args, **kwargs):
        self.activation_class = activation_class
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
