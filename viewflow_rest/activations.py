#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2020-11-06 00:01:40


class Activation(object):

    def __init__(self, *args, **kwargs):
        self.flow_class, self.flow_task = None, None
        self.process, self.task = None, None


class StartActivation(Activation):

    def initializer(self, flow_task, task):

        pass
