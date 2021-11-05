#!/usr/bin/env python
# coding: utf-8

from textwrap import dedent

from nbgrader.apps import NbGraderApp

from .exportapp import ExportApp


class AsyncNbGraderApp(NbGraderApp):
    """Custom nbgrader application to provide async capabilities to nbgrader's
    autograder.
    """

    name = "async_nbgrader-autograder"

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
