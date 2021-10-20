#!/usr/bin/env python
# coding: utf-8

import sys
import os

from textwrap import dedent

from traitlets import default
from traitlets.config.application import catch_config_error
from jupyter_core.application import NoStart

from nbgrader.apps import NbGraderApp

from .exportapp import ExportApp
from .processmessageapp import ProcessMessageApp


class AsyncNbGraderApp(NbGraderApp):

    name = u'async_nbgrader'

    subcommands = dict(
        export=(
            ExportApp,
            dedent(
                """
                Export grades from the database to another format.
                """
            ).strip()
        ),
        process_message=(
            ProcessMessageApp,
            dedent(
                """
                Handles base64 encoded messages
                """
            ).strip()
        ),
    )

def main():
    AsyncNbGraderApp.launch_instance()
