"""Tornado handlers for nbgrader background service."""
import os

from notebook.utils import url_path_join as ujoin

from .handlers import handlers
from .scheduler import scheduler


def _jupyter_nbextension_paths():
    return []


def _jupyter_server_extension_paths():
    return [
        dict(module="async_nbgrader"),
    ]


def rewrite(nbapp, x):
    web_app = nbapp.web_app
    pat = ujoin(web_app.settings["base_url"], x[0].lstrip("/"))
    return (pat,) + x[1:]


def load_jupyter_server_extension(nbapp):
    """Start background processor"""
    async_mode = os.environ.get("NBGRADER_ASYNC_MODE", "true")
    if async_mode == "true":
        nbapp.log.info("Starting background processor for nbgrader serverextension")
        nbapp.web_app.add_handlers(".*$", [rewrite(nbapp, x) for x in handlers])
        scheduler.start()
    else:
        nbapp.log.info("Skipping background processor for nbgrader serverextension")
