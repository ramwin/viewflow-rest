import logging

from viewflow_rest import flows, nodes, rest_extensions, this
from viewflow_rest.signals import task_finished

from . import models, serializers


class DeprecatedFlow(flows.Flow):

    process_class = models.DeprecatedProcess
    task_class = models.DeprecatedTask

    start = nodes.Start(
        viewclass=rest_extensions.AutoCreateAPIView,
        serializer_class=serializers.BaseSerializer,
    ).Next(
        this.should_not_run
    )

    should_not_run = nodes.End()


deprecated_flow = DeprecatedFlow()


def always_raise(**kwargs):
    raise DeprecationWarning()


task_finished.connect(always_raise,
    sender=DeprecatedFlow,)
