import json
import os

from tornado import web

from nbgrader.server_extensions.formgrader.apihandlers import AutogradeHandler
from nbgrader.server_extensions.formgrader.base import check_notebook_dir
from nbgrader.server_extensions.formgrader.base import check_xsrf
from notebook.notebookapp import NotebookApp
from notebook.utils import url_path_join as ujoin

from .scheduler import scheduler
from .tasks import autograde_assignment


class AsyncAutogradeHandler(AutogradeHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def post(self, assignment_id: str, student_id: str) -> json:
        scheduler.add_job(
            autograde_assignment,
            "date",
            args=[
                self.settings["notebook_dir"],
                self.api.course_id,
                assignment_id,
                student_id,
            ],
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


def rewrite(nbapp: NotebookApp, x: str) -> str:
    """Rewrites a path to remove the trailing forward slash (/).

    Args:
        nbapp (NotebookApp): The Jupyter Notebook application instance.
        x (str): The path to rewrite.

    Returns:
        str: the re written path.
    """
    web_app = nbapp.web_app
    pat = ujoin(web_app.settings["base_url"], x[0].lstrip("/"))
    return (pat,) + x[1:]


def load_jupyter_server_extension(nbapp: NotebookApp) -> None:
    """Start background processor

    Args:
      nbapp (NotebookApp): The Jupyter Notebook application instance.
    """
    if os.environ.get("NBGRADER_ASYNC_MODE", "true") == "true":
        nbapp.log.info("Starting background processor for nbgrader serverextension")
        nbapp.web_app.add_handlers(".*$", [rewrite(nbapp, x) for x in handlers])
        scheduler.start()
    else:
        nbapp.log.info("Skipping background processor for nbgrader serverextension")
