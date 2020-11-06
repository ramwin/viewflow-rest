#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2020-11-05 21:06:54


import logging
from django.urls import path
from django.views.generic.base import RedirectView

from rest_framework.response import Response

from . import nodes, edges, activations


log = logging.getLogger(__name__)


class StartViewMixin(object):

    def activation_done(self, *args, **kwargs):
        self.activation.done()

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self.activation_done()

    def dispatch(self, request, **kwargs):
        flow_task = kwargs["flow_task"]
        activation = flow_task.activation_class()
        self.activation = request.activation = activation
        activation.initializer(flow_task)
        log.info("StartViewMixin.dispatch")
        log.info(f"kwargs: {kwargs}")
        return super().dispatch(request, **kwargs)

    def post(self, request, *args, **kwargs):
        request.activation.prepare()
        serializer = self.get_serializer(
            request.activation.process,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=201,
            headers=headers)
