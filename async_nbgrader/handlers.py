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


class FormgraderStaticHandler(IPythonHandler):
    def get(self):
        # this is a hack to override text in formgrader, we are appending our JS module to a module imported in formgrader
        original_data = pkgutil.get_data("nbgrader", "server_extensions/formgrader/static/js/utils.js").decode("utf-8")
        common_js = pkgutil.get_data(__name__, "static/common.js").decode("utf-8")
        self.write(original_data)
        self.write(common_js)
        self.set_header('Content-Type', 'application/javascript')
        self.finish()

handlers = [
    (r"/formgrader/api/submission/([^/]+)/([^/]+)/autograde", AsyncAutogradeHandler),
]

static_handlers = [
    (r"/formgrader/static/js/utils.js$", FormgraderStaticHandler),
]

def rewrite(nbapp, x):
    web_app = nbapp.web_app
    pat = ujoin(web_app.settings["base_url"], x[0].lstrip("/"))
    return (pat,) + x[1:]

def load_jupyter_server_extension(nbapp: NotebookApp):
    """Start background processor"""
    if os.environ.get("NBGRADER_ASYNC_MODE", "true") == "true":
        nbapp.log.info("Starting background processor for nbgrader serverextension")
        nbapp.web_app.add_handlers(".*$", [rewrite(nbapp, x) for x in handlers])
        scheduler.start()
    else:
        nbapp.log.info("Skipping background processor for nbgrader serverextension")
    nbapp.web_app.add_handlers(".*$", [rewrite(nbapp, x) for x in static_handlers])
