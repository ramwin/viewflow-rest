#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2020-11-05 21:06:54


import logging
from django.urls import path
from django.views.generic.base import RedirectView
from . import nodes, edges


log = logging.getLogger(__name__)


class ViewArgsMixin(object):

    def __init__(self, **kwargs):
        self._view_args = kwargs


class Start(nodes.Node, ViewArgsMixin):

    task_type = "START"

    def __init__(self, viewclass=None, *args, **kwargs):
        log.info("Start.init")
        log.info(args)
        log.info(kwargs)
        self._view = viewclass
        if viewclass is None:
            raise Exception("不对")
        super().__init__(viewclass, **kwargs)

    def _outgoing(self):
        if self._next:
            return [
                edges.Edge(src=self, dst=self._next, edge_class='next')
            ]
        return []

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


class End(nodes.Node):

    task_type = "END"

    def _outgoing(self):
        return []
