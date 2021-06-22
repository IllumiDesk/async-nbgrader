"""Tornado handlers for nbgrader background service."""
from .handlers import load_jupyter_server_extension


def _jupyter_nbextension_paths():
    return [
        dict(
            section="common",
            src="static",
            dest="async_nbgrader/static",
            require="async_nbgrader/static/common"
        ),
    ]

def _jupyter_server_extension_paths():
    return [
        dict(module="async_nbgrader"),
    ]
