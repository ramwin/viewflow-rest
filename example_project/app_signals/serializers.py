
from rest_framework import serializers

from . import models


class BaseSerializer(serializers.Serializer):

    class Meta:
        fields = []
