#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2020-11-05 21:06:54


import logging
from django.urls import path
from django.views.generic.base import RedirectView
from . import nodes, edges, activations


log = logging.getLogger(__name__)


class StartViewMixin(object):

    def activation_done(self, *args, **kwargs):
        self.kwargs['flow_task'].done()

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self.request.activation.process = serializer.instance

    def dispatch(self, request, *args, **kwargs):
        log.info("StartViewMixin.dispatch")
        log.info(f"args: {args}")
        log.info(f"kwargs: {kwargs}")
        activation = activations.Activation()
        # activation.
        request.activation = activation
        return super().dispatch(request, *args, **kwargs)
