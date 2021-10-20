# coding: utf-8

import base64
import json

from traitlets import default
from nbgrader.apps.baseapp import NbGrader
from ..helpers import get_nbgrader_api

aliases = {
    "log-level": "Application.log_level",
}
flags = {}


class ProcessMessageApp(NbGrader):

    name = u"async_nbgrader-process-message"

    aliases = aliases

    @default("classes")
    def _classes_default(self):
        classes = super(ProcessMessageApp, self)._classes_default()
        classes.append(ProcessMessageApp)
        return classes

    def start(self):
        super(ProcessMessageApp, self).start()
        if len(self.extra_args) == 0 or self.extra_args[0] == "":
            self.fail("message is missing")
        message = json.loads(self.extra_args[0])
        encoded_message = message["data"]
        self.log.info("message " + encoded_message)
        missing_padding = len(encoded_message) % 4
        if missing_padding > 0:
            encoded_message += (b'=' * (4 - missing_padding))
        body = json.loads(base64.b64decode(encoded_message).decode('utf-8')).get("body")
        if body == None:
            self.fail("body is missing")
        action = body.get("action")
        notebook_dir = body.get("notebook_dir")
        course_id = body.get("course_id")
        api = get_nbgrader_api(notebook_dir, course_id)
        if action == "autograde":
            assignment_id = body.get("assignment_id")
            student_id = body.get("student_id")
            api.autograde(assignment_id, student_id)
        else:
            self.fail("message is missing")