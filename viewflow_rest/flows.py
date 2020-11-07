#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2020-11-05 19:36:00


from collections import defaultdict
import logging

from django.urls import re_path, include

from . import models, This, ThisObject
from .nodes import Node


log = logging.getLogger(__name__)


log.debug("引入viewflow_rest.flows.py")


class _Resolver(object):

    def __init__(self, nodes):
        self.nodes = nodes

    def get_implementation(self, link):
        if isinstance(link, Node):
            node = link
        elif isinstance(link, ThisObject):
            node = self.nodes.get(link.name)
        elif isinstance(link, str):
            node = self.nodes.get(link)
        if node:
            return node
        raise Exception(f"没有node{link}啊")


class FlowMeta(object):
    def __init__(self, app_label, flow_class, nodes):
        self.app_label = app_label
        self.flow_class = flow_class
        self._nodes_by_name = nodes

    def nodes(self):
        return self._nodes_by_name.values()


class FlowMetaClass(type):

    def __new__(cls, class_name, bases, attrs, **kwargs): 
        log.debug("创建一个新的Flow类")
        log.debug(attrs)
        new_class = super(FlowMetaClass, cls).__new__(
            cls, class_name, bases, attrs)

        nodes = {}
        # 根据Flow的属性，初始化nodes
        for name, attr in attrs.items():
            if isinstance(attr, Node):
                nodes[name] = attr

        # 设定node的name
        for name, node in nodes.items():
            node.name = name

        resolver = _Resolver(nodes)
        for node in nodes.values():
            node._resolve(resolver)

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

        for name, node in nodes.items():
            node.flow_class = new_class

        app_label = None
        new_class._meta = FlowMeta(app_label, new_class, nodes)
        for name, node in nodes.items():
            node.flow_class = new_class

        for name, node in nodes.items():
            node.ready()

        return new_class


log.debug("初始化Flow")


class Flow(metaclass=FlowMetaClass):

    process_class = None
    task_class = None
    process_title = None

    @property
    def urls(self):
        log.debug("载入Flow.urls")
        node_urls = []
        for node in self._meta.nodes():
            node_urls += node.urls()
        result = node_urls
        log.debug("载入Flow.urls完毕")
        log.debug(result)
        return result

    def __str__(self):
        return str(self.process_title)


log.debug("引入viewflow_rest.flows.py结束")


this = This()
