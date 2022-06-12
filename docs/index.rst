.. viewflow-rest documentation master file, created by
   sphinx-quickstart on Sun Jun 12 12:43:58 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to viewflow-rest's documentation!
=========================================

you can fork the project from `github <https://github.com/ramwin/viewflow-rest/>`

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Quick Start
===========
use the `example_project` as a example::

    git clone git@github.com:ramwin/viewflow-rest.git  
    cd vieflow-rest/example_project/
    sudo pip3 install -r ./requirements.txt
    python3 manage.py migrate
    python3 manage.py runserver
    # visit http://localhost:8000/exam/ or http://localhost:8000/hire/ to get the api


Tutorial
========

exam flow
^^^^^^^^^

.. image:: ../example_project/exam_flow.png

this graph like above picture can be written like the below code::

    # example_project/exam/flows.py
    class ExamFlow(flows.Flow):

        process_class = models.ExamProcess
        task_class = models.ExamTask

        register = nodes.Start(
            viewclass=rest_extensions.AutoCreateAPIView,
            serializer_class=serializers.RegisterExamSerializer,
        ).Next(
            this.select_term
        )

        select_term = nodes.View(
            viewclass=rest_extensions.AutoUpdateAPIView,
            fields=["term"],
        ).Next(this.take_exam)

        take_exam = nodes.View(
            viewclass=rest_extensions.AutoUpdateAPIView,
            fields=["grade"],
        ).Next(this.check_grade)

        check_grade = nodes.If(
            cond=lambda activation: activation.process.passed
        ).Then(this.end).Else(this.select_term)
        end = nodes.End()


quite simple and intuitive, right?


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


API Reference
=============

.. autoclass: viewflow_rest.flows.Flow

