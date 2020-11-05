#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2020-11-05 22:11:42


import logging


log = logging.getLogger(__name__)


class ThisObject(object):

    def __init__(self, name):
        self.name = name

class This(object):

    def __getattr__(self, name):
        return ThisObject(name)


this = This()
