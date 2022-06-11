#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


from rest_framework import serializers
from . import models


class RegisterExamSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ExamProcess
        fields = ["id", "subject"]
