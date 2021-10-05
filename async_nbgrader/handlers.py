import json
import os
import pkgutil

from tornado import web

from nbgrader.server_extensions.formgrader.apihandlers import AutogradeHandler
from nbgrader.server_extensions.formgrader.base import check_xsrf, check_notebook_dir
from notebook.base.handlers import IPythonHandler
from notebook.notebookapp import NotebookApp
from notebook.utils import url_path_join as ujoin

from .scheduler import scheduler
from .tasks import autograde_assignment


class AsyncAutogradeHandler(AutogradeHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def post(self, assignment_id, student_id):
        scheduler.add_job(
            autograde_assignment, "date", args=[None, assignment_id, student_id]
        )
        self.write(
            json.dumps(
                {
                    "success": True,
                    "queued": True,
                    "message": "Submission Autograding queued",
                }
            )
        )


handlers = [
    (r"/formgrader/api/submission/([^/]+)/([^/]+)/autograde", AsyncAutogradeHandler),
]

def rewrite(nbapp, x):
    web_app = nbapp.web_app
    pat = ujoin(web_app.settings["base_url"], x[0].lstrip("/"))
    return (pat,) + x[1:]

def load_jupyter_server_extension(nbapp: NotebookApp):
    """Start background processor"""
    if os.environ.get("NBGRADER_ASYNC_MODE", "false") == "true":
        nbapp.log.info("Starting background processor for nbgrader serverextension")
        nbapp.web_app.add_handlers(".*$", [rewrite(nbapp, x) for x in handlers])
        scheduler.start()
    else:
        nbapp.log.info("Skipping background processor for nbgrader serverextension")
    nbapp.web_app.add_handlers(".*$", [rewrite(nbapp, x) for x in static_handlers])
