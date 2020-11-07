#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2020-11-07 21:31:32


class PermissionMixin(object):

    def __init__(self, *args, **kwargs):
        self._owner_group = None
        super().__init__(*args, **kwargs)

    def Permission(self, group=None):
        """
        if a Node should be performed only by a certain group
        
            from django.contrib.auth.models import Group
            nodes.View(
                viewclass
            ).Permission(
                group=Group.objects.get(name="hr")
            )
        """

        self._owner_group = group
        return self
