#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2020-11-05 21:06:54


import logging
from django.urls import path
from django.views.generic.base import RedirectView
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from . import nodes, edges, activations


log = logging.getLogger(__name__)


class StartViewMixin(object):

    def activation_done(self, *args, **kwargs):
        self.activation.done(operator=self.request.user)

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self.activation_done()

    def dispatch(self, request, **kwargs):
        flow_task = kwargs["flow_task"]
        activation = flow_task.activation_class()
        self.activation = request.activation = activation
        activation.initialize(flow_task)
        if not self.activation.has_perm(request.user):
            raise PermissionDenied
        log.debug("StartViewMixin.dispatch")
        log.debug(f"kwargs: {kwargs}")
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


class UpdateViewMixin(object):

    def activation_done(self, *args, **kwargs):
        self.activation.done(operator=self.request.user)

    def perform_update(self, serializer):
        log.debug("数据更新开始")
        super().perform_update(serializer)
        log.debug("数据更新完毕")
        self.activation_done()

    def dispatch(self, request, **kwargs):
        flow_task = kwargs["flow_task"]
        task_pk = kwargs["task_id"]
        process_pk = kwargs["process_id"]

        task = get_object_or_404(
            flow_task.flow_class.task_class._default_manager,
            pk=task_pk,
            flow_task=flow_task.name,
            process_id=process_pk,
        )

        activation = flow_task.activation_class()
        self.activation = request.activation = activation
        activation.initialize(flow_task, task)
        if not activation.has_perm(request.user):
            raise PermissionDenied

        return super().dispatch(request, **kwargs)

    def post(self, request, *args, **kwargs):
        request.activation.prepare()
        serializer = self.get_serializer(
            request.activation.process,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        # headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=200)
