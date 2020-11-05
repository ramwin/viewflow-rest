#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2020-11-05 19:51:05


class Node(object):

    def __init__(self, activation_class=None):
        self.activation_class = activation_class
        self._incoming_edges = []
        self._next = None

    def Next(self, node):
        self._next = node

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


class Start(Node):

    task_type = "START"

    def __init__(self, view_or_class=None, **kwargs):
        self._view = view_or_class
        super().__init__(view_or_class, **kwargs)
