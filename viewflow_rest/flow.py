#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2020-11-05 19:36:00


from . import models
from .nodes import Node


class FlowMetaClass(type):

    def __new__(cls, class_name, bases, attrs, **kwargs): 
        nodes = {}
        # 根据Flow的属性，初始化nodes
        for name, attr in attrs.items():
            if isintance(attr, Node):
                nodes[name] = attr

        # 设定node的name
        for name, node in nodes.items():
            node.name = name

        # 设定node的_incoming_edges
        # key为outgoing的node
        incoming = defaultdict(list)
        # A ---e---> B
        # e.src = A;  e.dst = B
        # incoming = {B: [e]}
        for _, node in nodes.items():
            for outgoing_edge in node._outgoing():
                incoming[outgoing_edge.dst].append(outgoing_edge)
        for node, edges in incoming.items():
            node._incoming_edges = edges


class Flow(metaclass=FlowMetaClass):

    process_class = models.Process
    task_class = models.Task
