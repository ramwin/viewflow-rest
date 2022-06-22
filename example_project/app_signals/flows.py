import logging
import warnings

from viewflow_rest import flows, nodes, rest_extensions, this
from viewflow_rest.signals import task_finished, task_started

from . import models, serializers


logger = logging.getLogger(__name__)


class DeprecatedFlow(flows.Flow):

    process_class = models.DeprecatedProcess
    task_class = models.DeprecatedTask

    start = nodes.Start(
        viewclass=rest_extensions.AutoCreateAPIView,
        serializer_class=serializers.BaseSerializer,
    ).Next(
        this.warning
    )
    warning = nodes.View(
        viewclass=rest_extensions.AutoCreateAPIView,
        serializer_class=serializers.BaseSerializer,
    ).Next(
        this.error
    )
    error = nodes.View(
        viewclass=rest_extensions.AutoCreateAPIView,
        serializer_class=serializers.BaseSerializer,
    ).Next(
        this.end
    )

    end = nodes.End()


deprecated_flow = DeprecatedFlow()


def only_warning(**kwargs):
    warnings.warn("warning: do not continue anymore!!!!!")
    logger.warning(kwargs)

def always_raise(**kwargs):
    logger.error("error!!!")
    raise DeprecationWarning()


task_finished.connect(always_raise,
    sender=DeprecatedFlow.error)

task_finished.connect(only_warning,
    sender=DeprecatedFlow.warning)

task_started.connect(only_warning,
    sender=DeprecatedFlow.warning)
    
task_started.connect(only_warning,
    sender=DeprecatedFlow.error)