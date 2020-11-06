#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2020-11-05 19:46:45


from django.db.models import TextChoices


class Edge(object):
    """流程图里面的每一条边"""

    def __init__(self, src, dst, edge_class):
        """
        edge_class: next代表直接下一步
            cond_true: 代表为true才执行
            cond_false: 代表为false才执行
        """
        self._src = src
        self._dst = dst
        self._edge_class = edge_class

    @property
    def src(self):
        return self._src

    @property
    def dst(self):
        return self._dst

    @property
    def edge_class(self):
        return self._edge_class

    def __str__(self):
        return f"[{self.edge_class}] {self.src} ---> {self.dst}"


class STATUS_CHOICE(TextChoices):
    NEW = "NEW", "创建了"
    STARTED = "STARTED", "开始了"
    DONE = "DONE", "结束了"
    CANCELED = "CANCELED", "取消了"
