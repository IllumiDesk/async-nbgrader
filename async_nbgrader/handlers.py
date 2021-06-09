import json

from tornado import web

from nbgrader.server_extensions.formgrader.apihandlers import AutogradeHandler
from nbgrader.server_extensions.formgrader.base import check_xsrf, check_notebook_dir

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
