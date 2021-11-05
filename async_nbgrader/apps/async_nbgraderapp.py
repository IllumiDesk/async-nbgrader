#!/usr/bin/env python
# coding: utf-8

from textwrap import dedent

from traitlets import default
from traitlets.config.application import catch_config_error
from jupyter_core.application import NoStart

from nbgrader.apps import NbGraderApp

from .exportapp import ExportApp


class AsyncNbGraderApp(NbGraderApp):
    """Custom nbgrader application to provide async capabilities to nbgrader's
    autograder.
    """

    name = u"async_nbgrader-autograder"

    subcommands = dict(
        export=(
            ExportApp,
            dedent(
                """
                Export grades from the database to another format.
                """
            ).strip(),
        ),
    )


def main():
    AsyncNbGraderApp.launch_instance()
